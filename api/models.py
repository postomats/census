from ormar import String, Integer, Model, DateTime
from db import BaseMeta
import datetime, bcrypt


class User(Model):
    """
    Класс, представляющий пользователя.

    Содержит информацию о пользователе и методы для работы с учетной записью.
    """

    id: int = Integer(primary_key=True)
    created_date: datetime.datetime = DateTime(default=datetime.datetime.now)

    username = String(max_length=100, unique=True)
    first_name = String(max_length=100)
    last_name = String(max_length=100)
    email = String(max_length=100, unique=True)

    password = String(max_length=255)

    async def set_password(self, password: str) -> None:
        """
        Устанавливает пароль пользователя.

        :param password: Новый пароль.
        """
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    async def check_password(self, password: str) -> bool:
        """
        Проверяет соответствие введенного пароля текущему паролю пользователя.

        :param password: Пароль для проверки.
        :return: True, если пароль верен, в противном случае - False.
        """
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    class Meta(BaseMeta):
        """
        Метакласс для определения настроек таблицы базы данных для модели User.
        """

        tablename = "users_db"

    async def json(self):
        """
        Преобразует объект User в словарь.

        :return: Словарь с данными объекта User.
        """
        return {
            "id": self.id,
            "created": self.created_date,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
