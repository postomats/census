from os import env

jwt_key = "pass"
KEYS = ['POSTGRES_USER', 'POSTGRES_PASSWORD',
        'POSTGRES_HOSTNAME', 'POSTGRES_DB']
USER, PASSWORD, HOSTNAME, DATABASE = (env.get(i, 'test') for i in KEYS)
SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOSTNAME}/{DATABASE}'