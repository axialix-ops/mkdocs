from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Кошелек(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    id_владельца = Column(Integer, ForeignKey("users.id"))
    валюта = Column(String, nullable=False)
    баланс = Column(Float, default=0.0)

    владелец = relationship("Пользователь", back_populates="кошельки")
