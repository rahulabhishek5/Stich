from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import crud
from database import get_db

# -------------------------
# 1. JWT Settings
# -------------------------
SECRET_KEY = "replace_this_with_a_long_random_secret"  # keep in .env in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# -------------------------
# 2. Password Context
# -------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# -------------------------
# 3. Password Utilities
# -------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if provided password matches hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)

# -------------------------
# 4. Authenticate User
# -------------------------
def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user using email and password.
    Returns User object if successful, else None.
    """
    user = crud.get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# -------------------------
# 5. JWT Access Token
# -------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT token with payload data and optional expiry.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# -------------------------
# 6. Current User Dependency
# -------------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    FastAPI dependency to get current user from JWT token.
    Raises 401 if invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

# -------------------------
# 7. Role-based Access Helpers
# -------------------------
def get_current_active_user(current_user=Depends(get_current_user)):
    """
    Ensure the user is active.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_teacher(current_user=Depends(get_current_active_user)):
    """
    Ensure the user is a teacher (or admin).
    """
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="User does not have teacher privileges")
    return current_user

def get_current_admin(current_user=Depends(get_current_active_user)):
    """
    Ensure the user is an admin.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="User is not admin")
    return current_user
