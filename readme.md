# FastAPI Auth API 🔐

A simple authentication system using FastAPI, SQLAlchemy, JWT, and OTP.

## 🚀 Features

- User registration with OTP verification
- JWT-based login (access & refresh tokens)
- Resend OTP
- Forgot & reset password via OTP
- Protected route with token auth

## 📦 Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- Passlib (bcrypt)
- JWT

## 📂 Key Endpoints

| Method | Endpoint             | Description                        |
|--------|----------------------|------------------------------------|
| POST   | `/auth/register`     | Register user and send OTP         |
| POST   | `/auth/verify`       | Verify OTP to complete registration |
| POST   | `/auth/login`        | Login and receive tokens           |
| POST   | `/auth/resend`       | Resend OTP                         |
| POST   | `/auth/forgot-password` | Send OTP to reset password       |
| POST   | `/auth/reset-password`  | Reset password using OTP         |
| GET    | `/auth/protected`    | Access protected route             |

## 🛠️ Setup

```bash
git clone https://github.com/jiporCK/fastapi-authentication-template.git
cd project
pip install -r requirements.txt
uvicorn main:app --reload

✅ Notes
Configure email + JWT secret in .env or directly in code.
Extend with roles, refresh token rotation, or rate limiting as needed.
