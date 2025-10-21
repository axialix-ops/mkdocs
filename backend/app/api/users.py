from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import создать_токен_доступа, получить_хэш_пароля, проверить_пароль
from app.models.user import Пользователь
from app.schemas.user import СозданиеПользователя, Пользователь as СхемаПользователя, Токен
from app.api.deps import получить_дб
from app.api.wallet import создать_кошелек_пользователя

router = APIRouter()

@router.post("/register", response_model=СхемаПользователя, summary="Регистрация нового пользователя")
def зарегистрировать_пользователя(пользователь: СозданиеПользователя, дб: Session = Depends(получить_дб)):
    """
    Регистрирует нового пользователя в системе и создает для него виртуальные кошельки.
    """
    дб_пользователь = дб.query(Пользователь).filter(Пользователь.email == пользователь.email).first()
    if дб_пользователь:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже зарегистрирован")

    хэшированный_пароль = получить_хэш_пароля(пользователь.password)
    дб_пользователь = Пользователь(email=пользователь.email, хэш_пароля=хэшированный_пароль)
    дб.add(дб_пользователь)
    дб.commit()
    дб.refresh(дб_пользователь)

    создать_кошелек_пользователя(дб, дб_пользователь)

    return дб_пользователь

@router.post("/login", response_model=Токен, summary="Аутентификация пользователя")
def войти_для_получения_токена(дб: Session = Depends(получить_дб), форма_данных: OAuth2PasswordRequestForm = Depends()):
    """
    Аутентифицирует пользователя и возвращает JWT токен доступа.
    """
    пользователь = дб.query(Пользователь).filter(Пользователь.email == форма_данных.username).first()
    if not пользователь or not проверить_пароль(форма_данных.password, пользователь.хэш_пароля):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    токен_доступа = создать_токен_доступа(data={"sub": пользователь.email})
    return {"access_token": токен_доступа, "token_type": "bearer"}
