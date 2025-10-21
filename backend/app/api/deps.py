from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.security import СЕКРЕТНЫЙ_КЛЮЧ, АЛГОРИТМ
from app.db.session import SessionLocal
from app.models.user import Пользователь
from app.schemas.user import ДанныеТокена

oauth2_схема = OAuth2PasswordBearer(tokenUrl="api/users/login")

def получить_дб():
    дб = SessionLocal()
    try:
        yield дб
    finally:
        дб.close()

def получить_текущего_пользователя(дб: Session = Depends(получить_дб), токен: str = Depends(oauth2_схема)):
    исключение_аутентификации = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        полезная_нагрузка = jwt.decode(токен, СЕКРЕТНЫЙ_КЛЮЧ, algorithms=[АЛГОРИТМ])
        email: str = полезная_нагрузка.get("sub")
        if email is None:
            raise исключение_аутентификации
        данные_токена = ДанныеТокена(email=email)
    except JWTError:
        raise исключение_аутентификации
    пользователь = дб.query(Пользователь).filter(Пользователь.email == данные_токена.email).first()
    if пользователь is None:
        raise исключение_аутентификации
    return пользователь
