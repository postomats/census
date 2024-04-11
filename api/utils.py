from sqlalchemy import select
from api.models import User
import jwt
<<<<<<< HEAD
=======
from api import models
>>>>>>> 0653682 (commit rewrite on sqlalchemy)
from api.SETTINGS import JWT_KEY

async def check_username_unique(username: str) -> bool:
    """
    Проверяет уникальность имени пользователя.

    :param username: Имя пользователя для проверки.
    :return: True, если имя уникально, в противном случае - False.
    """
    async with models.database.session() as session:
        return not await session.execute(select(User).filter(User.username == username)).scalar()

async def check_email_unique(email: str) -> bool:
    """
    Проверяет уникальность электронной почты.

    :param email: Адрес электронной почты для проверки.
    :return: True, если адрес уникален, в противном случае - False.
    """
    async with models.database.session() as session:
        return not await session.execute(select(User).filter(User.email == email)).scalar()

async def get_user_from_token(token: str):
    """
    Получает пользователя по токену.

    :param token: Токен для декодирования.
    :return: Объект пользователя, соответствующий идентификатору из токена.
    """
<<<<<<< HEAD
    payload = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
    user_id = payload.get('user_id')
    return await user.objects.get_or_none(id=user_id)
=======
    async with models.database.session() as session:
        payload = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        return await session.execute(select(User).filter(User.id == user_id)).scalar()
>>>>>>> 0653682 (commit rewrite on sqlalchemy)
