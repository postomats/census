from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.controller import controller
from os import environ
# Создание экземпляра FastAPI
app = FastAPI()
openapi_url = environ.get('OPENAPI_URL', '')
# Подключение роутера из модуля api.controller с префиксом и тегом
app.include_router(controller, tags=["Переписчик)"], openapi_url=openapi_url)

# Добавление middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 27012022
