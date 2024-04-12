from api.models import User
from db import SessionLocal

admin = User(
        first_name='admin',
        last_name='admin',
        group='',
        email='admin@admin.ru',
        password='admin',
        role='Admin',
        )

admin.set_password(password='admin')
db = SessionLocal()

try:
    if not db.query(User).filter(User.email == 'admin@admin.ru').first():
        db.add(admin)
        db.commit()
except Exception as e:
    print(e)