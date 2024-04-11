from api import utils
from api.models import User
import jwt
from fastapi import HTTPException
from api import schemas
from api.SETTINGS import JWT_KEY
from sqlalchemy.orm import Session


def create_user(
    db: Session,
    first_name: str,
    last_name: str,
    group: str,
    email: str,
    password: str,
    role: str,
):
    """
    Создает нового пользователя в базе данных и соответствующую папку для хранения данных.

    Parameters:
    - username (str): Имя пользователя.
    - first_name (str): Имя пользователя.
    - last_name (str): Фамилия пользователя.
    - email (str): Электронная почта пользователя.
    - password (str): Пароль пользователя.

    Returns:
    - dict: Возвращает статус регистрации и идентификатор пользователя, если успешно, или словарь с ошибкой.
    """
    if not utils.check_email_unique(db, email):
        raise HTTPException(status_code=400, detail="Почта не уникальна.")
    user = User(
        first_name=first_name,
        last_name=last_name,
        group=group,
        email=email,
        password=JWT_KEY,
        role=role,
    )
    user.set_password(password=password)

    try:
        db.add(user)
        db.commit()
    except:
        raise HTTPException(status_code=400, detail="Данные не уникальны.")
    return {"status": True, "user_id": user.id}


def sign_in(db, email: str, password: str):
    """
    Авторизует пользователя.

    Parameters:
    - email (str): Электронная почта пользователя.
    - password (str): Пароль пользователя.

    Returns:
    - dict: Возвращает токен аутентификации, если успешно, или словарь с ошибкой.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден по почте.")
    if user.check_password(password):
        return {"token": jwt.encode({"user_id": user.id}, JWT_KEY, algorithm="HS256")}
    raise HTTPException(status_code=401, detail="Пароль не верный.")


def reset_password(db, user, old: str, new: str) -> schemas.ResetPasswordReturn:
    """
    Сбрасывает пароль пользователя.

    Parameters:
    - user (User): Объект пользователя.
    - old (str): Старый пароль пользователя.
    - new (str): Новый пароль пользователя.

    Returns:
    - dict: Возвращает статус сброса пароля или словарь с ошибкой.
    """
    if old == new:
        raise HTTPException(status_code=400, detail="Новый пароль совпадает со старым.")
    if user.check_password(old):
        user.set_password(new)
        db.commit()
        return {"status": True}
    raise HTTPException(status_code=401, detail="Пароль не верный.")

