from sqlalchemy.orm import Session
from app.auth import models as auth_models  # ✅ Absolute import
from fastapi import HTTPException
from app.auth.models import User

def get_all_users(db: Session):
    users = db.query(auth_models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

def delete_user(user_id: int, db: Session):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"msg": "User deleted"}