from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, get_db
from app.auth.schemas import LoginRequest, OTPVerifyRequest, TokenResponse, RegisterRequest, ForgotPasswordAndResendOtpRequest, ResetPasswordRequest
from app.auth.service import register_user, verify_otp_and_create_user, login_user, forgot_password, reset_password, resend_otp
from app.auth.security import decode_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", response_model=dict)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user and send OTP.
    """
    return register_user(payload.email, payload.password, db)

@router.post("/verify", response_model=dict)
def verify(payload: OTPVerifyRequest, db: Session = Depends(get_db)):
    """
    Verify OTP and complete user registration.
    """
    return verify_otp_and_create_user(payload.email, payload.otp, db)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and issue access and refresh tokens.
    """
    return login_user(payload.email, payload.password, db)

@router.post("/resend")
def resend_otp(payload: ForgotPasswordAndResendOtpRequest, db: Session = Depends(get_db)):
    return resend_otp(payload.email, db)

@router.post("/forgot-password")
def forgot_password_user(payload: ForgotPasswordAndResendOtpRequest, db: Session = Depends(get_db)):
    return forgot_password(payload.email, db)

@router.post("/reset-password")
def reset_password_user(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_password(
        payload.email, 
        payload.otp, 
        payload.new_password,
        payload.confirm_new_password,
        db
        )

@router.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("user_id")
    # role = payload.get("role")
    return {"message": f"Protected route for user_id: {user_id}"}