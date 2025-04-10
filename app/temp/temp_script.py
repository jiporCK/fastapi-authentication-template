# temp_script.py
from db.database import engine, Base, SessionLocal
from auth.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)
db = SessionLocal()
new_user = User(email="srengchipor99@gmail.com", hashed_password=pwd_context.hash("Jipor@999"), otp=None)
db.add(new_user)
db.commit()
db.close()