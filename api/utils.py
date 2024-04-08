import jwt
from api.SETTINGS import jwt_key


async def check_username_unique(username: str, user: object) -> bool:
    """
    Проверяет уникальность имени пользователя.

    :param username: Имя пользователя для проверки.
    :param user: Объект пользователя для взаимодействия с базой данных.
    :return: True, если имя уникально, в противном случае - False.
    """
    return not await user.objects.filter(username=username).exists()


async def check_email_unique(email: str, user: object) -> bool:
    """
    Проверяет уникальность электронной почты.

    :param email: Адрес электронной почты для проверки.
    :param user: Объект пользователя для взаимодействия с базой данных.
    :return: True, если адрес уникален, в противном случае - False.
    """
    return not await user.objects.filter(email=email).exists()


async def get_user_from_token(token: str, user: object):
    """
    Получает пользователя по токену.

    :param token: Токен для декодирования.
    :param user: Объект пользователя для взаимодействия с базой данных.
    :return: Объект пользователя, соответствующий идентификатору из токена.
    """
    payload = jwt.decode(token, jwt_key, algorithms=['HS256'])
    user_id = payload.get('user_id')
    return await user.objects.get_or_none(id=user_id)