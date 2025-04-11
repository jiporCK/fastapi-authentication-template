from sqlalchemy.orm import Session
from app.auth import models as auth_models  # ✅ Absolute import
from fastapi import HTTPException

def get_all_users(db: Session):
    users = db.query(auth_models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users