from passlib.context import CryptContext

# Define the password hashing context to use bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Securely hash a password using bcrypt."""
    # Truncate to 72 chars to prevent Bcrypt 72-byte limit crashes
    safe_pwd = password[:72]
    return pwd_context.hash(safe_pwd)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hashed version."""
    safe_pwd = plain_password[:72]
    return pwd_context.verify(safe_pwd, hashed_password)

from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

# Constant values MVP
SECRET_KEY = "sentinel_mvp_ultra_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    """Sign and generate a new JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token returning the payload if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
