from pydantic import BaseModel, ConfigDict

class КошелекОснова(BaseModel):
    валюта: str
    баланс: float

class СозданиеКошелька(КошелекОснова):
    pass

class Кошелек(КошелекОснова):
    id: int
    id_владельца: int

    model_config = ConfigDict(from_attributes=True)
