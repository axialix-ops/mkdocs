from pydantic import BaseModel, ConfigDict
from typing import Optional

class ПользовательОснова(BaseModel):
    email: str

class СозданиеПользователя(ПользовательОснова):
    password: str

class Пользователь(ПользовательОснова):
    id: int
    активен: bool

    model_config = ConfigDict(from_attributes=True)

class Токен(BaseModel):
    access_token: str
    token_type: str

class ДанныеТокена(BaseModel):
    email: Optional[str] = None
