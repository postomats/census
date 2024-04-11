from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.controller import controller
import api.migrations

# Создание экземпляра FastAPI
app = FastAPI()

# Подключение роутера из модуля api.controller с префиксом и тегом
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
