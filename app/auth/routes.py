from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, get_db
from app.auth.schemas import LoginRequest, OTPVerifyRequest, TokenResponse, RegisterRequest
from app.auth.service import register_user, verify_otp_and_create_user, login_user
from app.auth.security import decode_token

router = APIRouter()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

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