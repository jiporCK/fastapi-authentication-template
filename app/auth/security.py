from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
import os
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_token(data: dict, expires_delta: timedelta, additional_claims: dict = None):
    """
    Create a JWT token with the given data and expiration.
    
    Args:
        data (dict): Base data to encode (e.g., {"sub": email})
        expires_delta (timedelta): Time until token expires
        additional_claims (dict, optional): Additional claims to include
    
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    if additional_claims:
        to_encode.update(additional_claims)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Optional: Function to decode token (for verification)
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None