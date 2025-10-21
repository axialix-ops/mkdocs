from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime

class Ордер(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    id_владельца = Column(Integer, ForeignKey("users.id"))
    символ = Column(String, nullable=False)
    сторона = Column(String, nullable=False)  # "ПОКУПКА" or "ПРОДАЖА"
    тип_ордера = Column(String, nullable=False) # "РЫНОЧНЫЙ", "ЛИМИТНЫЙ"
    количество = Column(Float, nullable=False)
    цена = Column(Float) # Цена исполнения для рыночного, цена лимита для лимитного
    статус = Column(String, default="В ОЖИДАНИИ") # В ОЖИДАНИИ, ИСПОЛНЕН, ОТМЕНЕН
    создан_в = Column(DateTime, default=datetime.datetime.utcnow)

    владелец = relationship("Пользователь")
