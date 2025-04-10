from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str