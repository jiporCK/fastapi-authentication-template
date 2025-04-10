from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_verified: bool
    
    class Config:
        orm_mode: True