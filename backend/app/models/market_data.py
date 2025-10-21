from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.base import Base
import datetime

class РыночныеДанные(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    символ = Column(String, nullable=False, index=True)
    метка_времени = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    цена_открытия = Column(Float, nullable=False)
    максимум = Column(Float, nullable=False)
    минимум = Column(Float, nullable=False)
    цена_закрытия = Column(Float, nullable=False)
    объем = Column(Float, nullable=False)
