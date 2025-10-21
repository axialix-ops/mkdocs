import os
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt

# Настройки безопасности из переменных окружения
СЕКРЕТНЫЙ_КЛЮЧ = os.getenv("SECRET_KEY", "your-secret-key")
АЛГОРИТМ = os.getenv("ALGORITHM", "HS256")
ВРЕМЯ_ЖИЗНИ_ТОКЕНА_МИНУТЫ = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

контекст_пароля = CryptContext(schemes=["bcrypt"], deprecated="auto")

def проверить_пароль(обычный_пароль, хэшированный_пароль):
    return контекст_пароля.verify(обычный_пароль, хэшированный_пароль)

def получить_хэш_пароля(пароль):
    return контекст_пароля.hash(пароль)

def создать_токен_доступа(данные: dict, время_жизни: Optional[timedelta] = None):
    кодируемые_данные = данные.copy()
    if время_жизни:
        время_истечения = datetime.utcnow() + время_жизни
    else:
        время_истечения = datetime.utcnow() + timedelta(minutes=ВРЕМЯ_ЖИЗНИ_ТОКЕНА_МИНУТЫ)
    кодируемые_данные.update({"exp": время_истечения})
    закодированный_jwt = jwt.encode(кодируемые_данные, СЕКРЕТНЫЙ_КЛЮЧ, algorithm=АЛГОРИТМ)
    return закодированный_jwt
