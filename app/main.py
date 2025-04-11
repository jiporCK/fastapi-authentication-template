from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.auth.routes import router as auth_router
from app.user.routes import router as user_router
from app.db.database import Base, engine, SessionLocal, get_db
from app.auth.models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(
    title="Authentication Service",
    description="A FastAPI service for user authentication with OTP",
    version="0.1.0"
)

# Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )

@app.on_event("startup")
async def startup_event():
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        # Insert initial user if not exists
        if not db.query(User).filter(User.email == "srengchipor99@gmail.com").first():
            new_user = User(
                email="srengchipor99@gmail.com",
                hashed_password=pwd_context.hash("Jipor@999"),
                role="admin"
            )
            db.add(new_user)
            db.commit()
            print("Initial user created successfully.")
        else:
            print("Initial user already exists, skipping creation.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error during startup: {e}")
        raise
    finally:
        db.close()


app.include_router(auth_router, prefix="/auth", dependencies=[Depends(get_db)])
app.include_router(user_router, dependencies=[Depends(get_db)])
