from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
from app.api.websockets import транслировать_обновления_цен
from app.core.market_data import генерировать_рыночные_данные

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Задачи, которые выполняются при старте приложения
    asyncio.create_task(транслировать_обновления_цен())
    asyncio.create_task(генерировать_рыночные_данные())
    yield
    # Задачи, которые выполняются при остановке (здесь не нужны)

app = FastAPI(
    title="Симулятор Криптобиржи",
    lifespan=lifespan,
    description="MVP симулятора криптобиржи с эмуляцией реальных графиков и торговлей.",
    version="0.1.0"
)

# Настройка CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
from app.api import users, wallet, trades, websockets
app.include_router(users.router, prefix="/api/users", tags=["Пользователи"])
app.include_router(wallet.router, prefix="/api/wallet", tags=["Кошелек"])
app.include_router(trades.router, prefix="/api/trades", tags=["Торговля"])
app.include_router(websockets.router, tags=["WebSocket"])


@app.get("/", summary="Root endpoint")
def read_root():
    return {"message": "Welcome to the Crypto Exchange Simulator API"}
