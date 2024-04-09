from api import models
from datetime import datetime
from api import utils
from api.models import User
import jwt
from api import exceptions
from api import schemas
from api.SETTINGS import jwt_key


async def create_user(
    username: str, first_name: str, last_name: str, group: str, email: str, password: str, role: str
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
    if not await utils.check_email_unique(email, User):
        return exceptions.sign_up_email_unique
    if not await utils.check_username_unique(username, User):
        return exceptions.sign_up_username_unique
    user = models.User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        group=group,
        email=email,
        password=jwt_key,
        role=role,
    )
    await user.set_password(password=password)
    user.created_date = datetime.now()

    try:
        await user.save()
    except:
        return exceptions.sign_up_error
    return {"status": True, "user_id": user.id}


async def sign_in(email: str, password: str):
    """
    Авторизует пользователя.

    Parameters:
    - email (str): Электронная почта пользователя.
    - password (str): Пароль пользователя.

    Returns:
    - dict: Возвращает токен аутентификации, если успешно, или словарь с ошибкой.
    """
    if not await User.objects.filter(email=email).exists():
        return exceptions.sign_in_user_not_found_by_email
    user = await User.objects.get(email=email)
    if await user.check_password(password):
        return {"token": jwt.encode({"user_id": user.id}, jwt_key, algorithm="HS256")}
    return exceptions.sign_in_wrong_password


async def reset_password(user, old: str, new: str) -> schemas.ResetPasswordReturn:
    """
    Сбрасывает пароль пользователя.

    Parameters:
    - user (User): Объект пользователя.
    - old (str): Старый пароль пользователя.
    - new (str): Новый пароль пользователя.

    Returns:
    - dict: Возвращает статус сброса пароля или словарь с ошибкой.
    """
    if await user.check_password(old):
        await user.set_password(new)
        await user.update()
        return {"status": True}
    return exceptions.sign_in_wrong_password
