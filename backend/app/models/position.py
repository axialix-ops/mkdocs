from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime

class Позиция(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    id_владельца = Column(Integer, ForeignKey("users.id"))
    символ = Column(String, nullable=False)
    количество = Column(Float, nullable=False)
    цена_входа = Column(Float, nullable=False)
    pnl = Column(Float, default=0.0)
    создана_в = Column(DateTime, default=datetime.datetime.utcnow)

    владелец = relationship("Пользователь", back_populates="позиции")
