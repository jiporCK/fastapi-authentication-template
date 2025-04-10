from sqlalchemy.orm import Session
from app.utils.emailer import send_otp_email
from app.auth.models import User
from app.auth.security import create_token
from datetime import timedelta
from fastapi import HTTPException
from passlib.context import CryptContext
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(email: str, password: str, db: Session):
    """
    Authenticate a user and generate/send an OTP.
    
    Args:
        email (str): User's email
        password (str): User's plain text password
        db (Session): SQLAlchemy database session
        
    Returns:
        dict: Message indicating OTP sent
        
    Raises:
        HTTPException: If credentials are invalid
    """
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, deails="Email already registered")
    
    otp = str(random.randint(100000, 999999))
    new_user = User(email= email, hashed_password=pwd_context.hash(password), otp=otp)
    db.add(new_user)
    db.commit()
    
    send_otp_email(email, otp)  # Replace mock print
    return {"msg": "OTP sent for registration. Please verify to complete registration."}

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def verify_otp_and_create_user(email: str, otp: str, db: Session):
    """
    Verify the OTP and issue tokens upon success.
    
    Args:
        email (str): User's email
        otp (str): One-time password
        db (Session): SQLAlchemy database session
        
    Returns:
        dict: Access and refresh tokens
        
    Raises:
        HTTPException: If OTP is invalid
    """
    user = db.query(User).filter(User.email == email, User.otp == otp).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")

    user.otp = None  # Clear OTP after successful verification
    user.is_verified = True
    db.commit()
    
    return {"msg": "User registered successfully"}

def login_user(email: str, password: str, db: Session):
    """
    Authenticate a user and issue access and refresh tokens.
    
    Args:
        email (str): User's email
        password (str): User's plain text password
        db (Session): SQLAlchemy database session
        
    Returns:
        dict: Access and refresh tokens
        
    Raises:
        HTTPException: If credentials are invalid
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    additional_claims = {
        "user_id": user.id
    }
    access_token = create_token({"sub": email}, timedelta(minutes=15), additional_claims)
    refresh_token = create_token({"sub": email}, timedelta(days=7), additional_claims)
    return {"access_token": access_token, "refresh_token": refresh_token}