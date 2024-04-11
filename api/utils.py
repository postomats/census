from api.models import User
import jwt
from api.SETTINGS import JWT_KEY
from sqlalchemy.orm import Session
def check_username_unique(db: Session, username: str) -> bool:
    """
    Проверяет уникальность имени пользователя.

    :param username: Имя пользователя для проверки.
    :return: True, если имя уникально, в противном случае - False.
    """
    return not db.query(User).filter(User.username == username).first()

def check_email_unique(db: Session, email: str) -> bool:
    """
    Проверяет уникальность электронной почты.

    :param email: Адрес электронной почты для проверки.
    :return: True, если адрес уникален, в противном случае - False.
    """
    return not db.query(User).filter(User.email == email).first()

def get_user_from_token(db: Session, token: str):
    """
    Получает пользователя по токену.

    :param token: Токен для декодирования.
    :return: Объект пользователя, соответствующий идентификатору из токена.
    """
    payload = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
    user_id = payload.get('user_id')
    return db.query(User).filter(User.id == user_id).first()
