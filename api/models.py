import bcrypt
from sqlalchemy import Column, String, Integer, DateTime, Enum
from datetime import datetime
from db import Base, engine

class User(Base):
    """
    Класс, представляющий пользователя.

    Содержит информацию о пользователе и методы для работы с учетной записью.
    """
    __tablename__ = 'users_db'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now)

    username = Column(String(100), unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100), unique=True)
    group = Column(String(100))
    password = Column(String(255))
    role = Column(Enum("Student", "Worker", "Admin", name="role_enum"))

    def set_password(self, password: str) -> None:
        """
        Устанавливает пароль пользователя.

        :param password: Новый пароль.
        """
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.password = hashed_password.decode("utf-8")

    def check_password(self, password: str) -> bool:
        """
        Проверяет соответствие введенного пароля текущему паролю пользователя.

        :param password: Пароль для проверки.
        :return: True, если пароль верен, в противном случае - False.
        """
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def json(self):
        """
        Преобразует объект User в словарь.

        :return: Словарь с данными объекта User.
        """
        return {
            "created": self.created_date,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "group": self.group,
            "email": self.email,
            "role": self.role
        }

Base.metadata.create_all(bind=engine)