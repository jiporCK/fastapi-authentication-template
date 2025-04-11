from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.emailer import send_otp_email
from app.auth.models import User, Otp
from app.auth.security import create_token
from datetime import timedelta, timezone, datetime
from fastapi import HTTPException
from passlib.context import CryptContext
from app.auth.security import decode_token
from app.db.database import SessionLocal, get_db
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("user_id")
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

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
    
    hashed_password = pwd_context.hash(password)
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    otp_code = str(random.randint(100000, 999999))
    otp = Otp(
        code = otp_code,
        user_id=new_user.id,
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5)
    )
    db.add(otp)
    db.commit()
    
    send_otp_email(email, otp_code)  # Replace mock print
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
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    stored_otp = db.query(Otp).filter(
        Otp.user_id == user.id,
        Otp.code == otp,
        Otp.expires_at >= datetime.now(timezone.utc)
    ).first()
    
    if not stored_otp:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")

    user.is_verified = True
    db.delete(stored_otp)
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

def resend_otp(email: str, db: Session):
    """
    Resend a new OTP to the user if not already verified.
    
    Args:
        email (str): User's email
        db (Session): SQLAlchemy session
    
    Returns:
        dict: Success message
    
    Raises:
        HTTPException: If user doesn't exist or is already verified
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_verified:
        raise HTTPException(status_code=400, detail="User is already verified")

    otp_code = str(random.randint(100000, 999999))
    
    existing_otp = db.query(Otp).filter(Otp.user_id == user.id).first()

    if existing_otp:
        # Update existing OTP
        existing_otp.code = otp_code
        existing_otp.created_at = datetime.now(timezone.utc)
        existing_otp.expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    else:
        # Create new OTP entry
        new_otp = Otp(
            code=otp_code,
            user_id=user.id,
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=5)
        )
        db.add(new_otp)

    db.commit()
    send_otp_email(email, otp_code)

    return {"msg": "A new OTP has been sent to your email."}

def forgot_password(email: str, db: Session):
    """
    Generates and sends an OTP for password reset.
    
    Args:
        email (str): User's email
        db (Session): SQLAlchemy database session
        
    Returns:
        dict: Message indicating OTP was sent
        
    Raises:
        HTTPException: If user does not exist
    """
    user = db.query(User).filter(
        User.email == email
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp_code = str(random.randint(100000, 999999))
    otp = Otp(
        code=otp_code,
        user_id=user.id,
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5)
    )
    db.add(otp)
    db.commit()
    send_otp_email(email, otp_code)
    return {"msg": "OTP sent to email for password reset."}

def reset_password(email: str, otp: str, new_password: str, confirm_new_password: str, db: Session):
    """
    Verifies the OTP and updates the user's password.
    
    Args:
        email (str): User's email
        otp (str): One-time password
        new_password (str): New password in plain text
        confirm_new_password (str): Confirmation of the new password
        db (Session): SQLAlchemy database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If OTP is invalid or user doesn't exist
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    stored_otp = db.query(Otp).filter(
        Otp.user_id == user.id,
        Otp.code == otp,
        Otp.expires_at >= datetime.now(timezone.utc)
    ).first()
    
    if not stored_otp:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    
    if new_password != confirm_new_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    user.hashed_password = pwd_context.hash(new_password)
    db.delete(stored_otp)
    db.commit()
    
    return {"msg": "Password reset successfully"}
