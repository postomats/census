from fastapi import APIRouter, Request, Depends
from pydantic import EmailStr

from api import schemas, utils, service
from api.models import User
from db import get_db
from sqlalchemy.orm import Session

controller = APIRouter()


@controller.post("/user/auth/sign-up")
def sign_up(
    request: Request,
    username: str = "username",
    first_name: str = "first_name",
    last_name: str = "last_name",
    group: str = "XXXXX",
    email: EmailStr = "email@email.email",
    password: str = "password",
    db: Session = Depends(get_db),
) -> schemas.SignInReturn | dict:
    """
    Регистрирует нового пользователя.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - username (str): Имя пользователя.
    - first_name (str): Имя пользователя.
    - last_name (str): Фамилия пользователя.
    - group (str): Учебная группа.
    - email (EmailStr): Электронная почта пользователя.
    - password (str): Пароль пользователя.

    Returns:
    - SignInReturn | dict: Возвращает данные о результате регистрации или словарь с ошибкой.
    """
    sign_up = service.create_user(
        db, username, first_name, last_name, group, email, password, role="Student"
    )
    if sign_up.get("status"):
        return service.sign_in(db, email, password)
    else:
        return sign_up


@controller.post("/user/auth/sign-in")
def sign_in(
    request: Request,
    email: EmailStr = "email@email.email",
    password: str = "password",
    db: Session = Depends(get_db),
) -> schemas.SignInReturn | dict:
    """
    Авторизует пользователя.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - email (EmailStr): Электронная почта пользователя.
    - password (str): Пароль пользователя.

    Returns:
    - SignInReturn | dict: Возвращает данные о результате авторизации или словарь с ошибкой.
    """
    return service.sign_in(db, email, password)


@controller.post("/user/reset_password")
def reset_password(
    request: Request, token: str, old: str, new: str, db: Session = Depends(get_db)
) ->  dict | schemas.ResetPasswordReturn:
    """
    Сбрасывает пароль пользователя.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для сброса пароля.
    - old (str): Старый пароль пользователя.
    - new (str): Новый пароль пользователя.

    Returns:
    - ResetPasswordReturn | dict: Возвращает данные о результате сброса пароля или словарь с ошибкой.
    """
    user: User = utils.get_user_from_token(db, token)
    return service.reset_password(db, user, old, new)


@controller.get("/me")
async def me(
    request: Request, token: str, db: Session = Depends(get_db)
) -> schemas.MeReturn | dict:
    """
    Получает информацию о текущем пользователе.

    Parameters:
    - request (Request): Объект запроса FastAPI.
    - token (str): Токен пользователя для аутентификации.

    Returns:
    - MeReturn | dict: Возвращает данные о текущем пользователе или словарь с ошибкой.
    """
    user: User = utils.get_user_from_token(db, token)
    return user.json()
