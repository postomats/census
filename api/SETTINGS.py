from os import environ as env

DEFAULT_KEY = "test"

JWT_KEY = "pass"
KEYS = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOSTNAME", "POSTGRES_DB"]
USER, PASSWORD, HOSTNAME, DATABASE = (env.get(i, DEFAULT_KEY) for i in KEYS)
SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOSTNAME}/{DATABASE}'
#SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"
JWT_KEY = env.get("JWT_KEY", DEFAULT_KEY)
