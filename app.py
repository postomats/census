from fastapi import FastAPI
import db as database
import sqlalchemy
from fastapi.middleware.cors import CORSMiddleware
from api.SETTINGS import SQLALCHEMY_DATABASE_URL
# Создание экземпляра FastAPI
app = FastAPI()

# Привязка объекта базы данных к экземпляру приложения
app.state.database = database.database

# Создание соединения с базой данных с использованием SQLAlchemy
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)

# Создание таблиц в базе данных при запуске приложения
database.metadata.create_all(engine)


# Подключение роутера из модуля api.controller с префиксом и тегом
from api.controller import controller

app.include_router(controller, tags=["Переписчик)"])

# Добавление middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 27012022
