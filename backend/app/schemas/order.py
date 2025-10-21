from pydantic import BaseModel, ConfigDict

class ОрдерОснова(BaseModel):
    символ: str
    сторона: str # "ПОКУПКА" or "ПРОДАЖА"
    тип_ордера: str # "РЫНОЧНЫЙ"
    количество: float

class СозданиеОрдера(ОрдерОснова):
    pass

class Ордер(ОрдерОснова):
    id: int
    id_владельца: int
    статус: str
    цена: float

    model_config = ConfigDict(from_attributes=True)
