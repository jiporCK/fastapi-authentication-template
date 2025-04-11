# 🔐 FastAPI Auth API

A secure authentication system built with **FastAPI**, **SQLAlchemy**, and **JWT**. Supports user registration with OTP, login, password reset, and protected routes.

---

## ⚙️ Features

- ✅ **User registration** with email + OTP verification
- 🔐 **JWT-based login** (access & refresh tokens)
- 🔁 **Resend OTP** functionality
- 🔑 **Forgot and Reset password** (with OTP verification)
- 🔒 **Protected routes** using reusable `get_current_user` dependency

---

## 📦 Tech Stack

- **FastAPI** – Web framework for building APIs
- **SQLAlchemy** – ORM for database handling
- **Pydantic** – Data validation and serialization
- **Passlib** (bcrypt) – Password hashing and security
- **JWT** (JSON Web Tokens) – Token-based authentication

---

## 📂 Endpoints

| Method | Endpoint              | Description                          |
|--------|-----------------------|--------------------------------------|
| POST   | `/auth/register`      | Register a new user and send OTP    |
| POST   | `/auth/verify`        | Verify OTP to complete registration |
| POST   | `/auth/login`         | Log in and receive JWT tokens       |
| POST   | `/auth/resend`        | Resend OTP                          |
| POST   | `/auth/forgot-password` | Send OTP to reset password        |
| POST   | `/auth/reset-password`  | Reset password using OTP           |
| GET    | `/auth/protected`     | Access a protected route            |
| DELETE | `/auth/admin/delete/{user_id}` | Admin deletes a user              |

---

## 🛠️ Setup Instructions

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd <project-folder>

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the FastAPI app
uvicorn main:app --reload
```

---

## 🔐 Using the Protected Route

After logging in, you'll receive an access token. Use this token to access protected routes by passing it in the `Authorization` header:

```bash
GET /auth/protected
Authorization: Bearer <access_token>
```

---

## 📋 Optional Improvements

- **Add refresh token rotation** for enhanced security.
- **Rate-limit OTP endpoints** to prevent abuse.
- **Role-based access** to protect certain routes for specific user roles (admin, etc.).
- **Switch to async DB with SQLModel** or **Tortoise ORM** for better performance.
