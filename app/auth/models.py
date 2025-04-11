from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from app.db.database import Base

class User(Base):
    __tablename__ = "users_tb"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)

    otps = relationship("Otp", back_populates="user", cascade="all, delete-orphan")


class Otp(Base):
    __tablename__ = "otp_tb"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5))

    user_id = Column(Integer, ForeignKey("users_tb.id"))  # ✅ FIX: add ForeignKey here
    user = relationship("User", back_populates="otps")
