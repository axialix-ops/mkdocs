import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.market_data import РыночныеДанные

router = APIRouter()

class МенеджерСоединений:
    def __init__(self):
        self.активные_соединения: dict[str, list[WebSocket]] = {}

    async def подключить(self, websocket: WebSocket, symbol: str):
        await websocket.accept()
        if symbol not in self.активные_соединения:
            self.активные_соединения[symbol] = []
        self.активные_соединения[symbol].append(websocket)

    def отключить(self, websocket: WebSocket, symbol: str):
        if symbol in self.активные_соединения:
            self.активные_соединения[symbol].remove(websocket)
            if not self.активные_соединения[symbol]:
                del self.активные_соединения[symbol]

    async def транслировать_свечу(self, данные_свечи: dict):
        symbol = данные_свечи.get("symbol")
        if symbol and symbol in self.активные_соединения:
            сообщение = json.dumps(данные_свечи)
            for соединение in self.активные_соединения[symbol]:
                await соединение.send_text(сообщение)

менеджер = МенеджерСоединений()

import random

async def транслировать_обновления_цен():
    """
    Асинхронная задача для трансляции данных о новых свечах всем подключенным WebSocket клиентам.
    """
    tracked_symbols = ['bitcoin', 'ethereum', 'ripple']
    last_candles = {}

    while True:
        try:
            price_data = cg.get_price(ids=tracked_symbols, vs_currencies='usd')

            for symbol in tracked_symbols:
                if symbol in price_data:
                    current_price = price_data[symbol]['usd']
                    now = int(time.time())

                    if symbol not in last_candles or (now - last_candles[symbol]['time']) >= 60:
                        # Новая свеча каждую минуту
                        last_candles[symbol] = {
                            "time": now,
                            "open": current_price,
                            "high": current_price,
                            "low": current_price,
                            "close": current_price,
                            "symbol": symbol,
                        }
                    else:
                        # Обновляем текущую свечу
                        last_candles[symbol]['high'] = max(last_candles[symbol]['high'], current_price)
                        last_candles[symbol]['low'] = min(last_candles[symbol]['low'], current_price)
                        last_candles[symbol]['close'] = current_price

                    await менеджер.транслировать_свечу(last_candles[symbol])

        except Exception as e:
            print(f"Error fetching prices from CoinGecko: {e}")

        await asyncio.sleep(10)

import os
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI

load_dotenv()
api_key = os.getenv("COINGECKO_API_KEY")
cg = CoinGeckoAPI(api_key=api_key)

@router.websocket("/ws/prices/{symbol}", name="ws_цены")
async def websocket_эндпоинт(websocket: WebSocket, symbol: str):
    """
    WebSocket эндпоинт для получения исторических и реал-тайм данных о свечах.
    """
    await менеджер.подключить(websocket, symbol)
    try:
        # Отправляем исторические данные при подключении
        ohlc_data = cg.get_coin_ohlc_by_id(id=symbol, vs_currency='usd', days=90)
        for entry in ohlc_data:
            candle_data = {
                "time": entry[0] / 1000,
                "open": entry[1],
                "high": entry[2],
                "low": entry[3],
                "close": entry[4],
                "symbol": symbol,
            }
            await websocket.send_text(json.dumps(candle_data))

        # Поддерживаем соединение открытым
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        менеджер.отключить(websocket, symbol)
