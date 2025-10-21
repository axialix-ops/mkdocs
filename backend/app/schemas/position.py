from pydantic import BaseModel, ConfigDict

class ПозицияОснова(BaseModel):
    символ: str
    количество: float
    цена_входа: float

class СозданиеПозиции(ПозицияОснова):
    pass

class Позиция(ПозицияОснова):
    id: int
    id_владельца: int
    pnl: float

    model_config = ConfigDict(from_attributes=True)
