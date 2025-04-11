# app/users/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db  # fixed: should be function, not `engine`

from app.user import schemas
from app.user import service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return service.get_all_users(db)
