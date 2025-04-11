# app/users/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db  # fixed: should be function, not `engine`
from app.auth.models import User
from app.user import schemas
from app.user import service
from app.auth import service as auth_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return service.get_all_users(db)

@router.delete("/delete/{user_id}")
def delete_user_as_admin(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.require_admin)):
    return service.delete_user(user_id, db)

