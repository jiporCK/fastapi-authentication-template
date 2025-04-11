from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, get_db
from app.auth.models import User
from app.auth.schemas import LoginRequest, OTPVerifyRequest, TokenResponse, RegisterRequest, ForgotPasswordAndResendOtpRequest, ResetPasswordRequest
from app.auth import service

router = APIRouter()

@router.post("/register", response_model=dict)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user and send OTP.
    """
    return service.register_user(payload.email, payload.password, db)

@router.post("/verify", response_model=dict)
def verify(payload: OTPVerifyRequest, db: Session = Depends(get_db)):
    """
    Verify OTP and complete user registration.
    """
    return service.verify_otp_and_create_user(payload.email, payload.otp, db)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and issue access and refresh tokens.
    """
    return service.login_user(payload.email, payload.password, db)

@router.post("/resend")
def resend_otp(payload: ForgotPasswordAndResendOtpRequest, db: Session = Depends(get_db)):
    return resend_otp(payload.email, db)

@router.post("/forgot-password")
def forgot_password_user(payload: ForgotPasswordAndResendOtpRequest, db: Session = Depends(get_db)):
    return service.forgot_password(payload.email, db)

@router.post("/reset-password")
def reset_password_user(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    return service.reset_password(
        payload.email, 
        payload.otp, 
        payload.new_password,
        payload.confirm_new_password,
        db
        )

@router.get("/protected")
def protected(current_user: User = Depends(service.get_current_user)):
    return {"msg": f"Welcome {current_user.email}"}
