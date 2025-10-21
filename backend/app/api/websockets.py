import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.market_data import РыночныеДанные

router = APIRouter()

class МенеджерСоединений:
    def __init__(self):
        self.активные_соединения: list[WebSocket] = []

    async def подключить(self, websocket: WebSocket):
        await websocket.accept()
        self.активные_соединения.append(websocket)

    def отключить(self, websocket: WebSocket):
        self.активные_соединения.remove(websocket)

    async def транслировать_свечу(self, данные_свечи: dict):
        сообщение = json.dumps(данные_свечи)
        for соединение in self.активные_соединения:
            await соединение.send_text(сообщение)

менеджер = МенеджерСоединений()

async def транслировать_обновления_цен():
    """
    Асинхронная задача для трансляции данных о новых свечах всем подключенным WebSocket клиентам.
    """
    дб: Session = SessionLocal()
    id_последней_трансляции = -1
    while True:
        # Получаем последнюю сгенерированную свечу
        последняя_свеча = дб.query(РыночныеДанные).order_by(РыночныеДанные.метка_времени.desc()).first()

        if последняя_свеча and последняя_свеча.id != id_последней_трансляции:
            данные_свечи = {
                "time": последняя_свеча.метка_времени.isoformat(),
                "open": последняя_свеча.цена_открытия,
                "high": последняя_свеча.максимум,
                "low": последняя_свеча.минимум,
                "close": последняя_свеча.цена_закрытия,
            }
            await менеджер.транслировать_свечу(данные_свечи)
            id_последней_трансляции = последняя_свеча.id

        await asyncio.sleep(1) # Проверяем наличие новой свечи каждую секунду

@router.websocket("/ws/prices", name="ws_цены")
async def websocket_эндпоинт(websocket: WebSocket):
    """
    WebSocket эндпоинт для получения исторических и реал-тайм данных о свечах.
    """
    await менеджер.подключить(websocket)
    try:
        # Отправляем исторические данные при подключении
        дб: Session = SessionLocal()
        история = дб.query(РыночныеДанные).order_by(РыночныеДанные.метка_времени.asc()).limit(300).all()
        for свеча in история:
            данные_свечи = {
                "time": свеча.метка_времени.isoformat(),
                "open": свеча.цена_открытия,
                "high": свеча.максимум,
                "low": свеча.минимум,
                "close": свеча.цена_закрытия,
            }
            await websocket.send_text(json.dumps(данные_свечи))

        # Поддерживаем соединение открытым
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        менеджер.отключить(websocket)
    finally:
        дб.close()
