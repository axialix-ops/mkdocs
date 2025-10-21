from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Пользователь(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    хэш_пароля = Column(String, nullable=False)
    активен = Column(Boolean(), default=True)

    кошельки = relationship("Кошелек", back_populates="владелец")
    позиции = relationship("Позиция", back_populates="владелец")
