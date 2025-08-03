from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
import bcrypt
import jwt
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User

router = APIRouter()
security = HTTPBearer()

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    user_type: str = "farmer"
    language_preference: str = "en"
    location: Optional[str] = None
    farm_size: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    user_type: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_pw = hash_password(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_pw,
        full_name=user_data.full_name,
        phone=user_data.phone,
        user_type=user_data.user_type,
        language_preference=user_data.language_preference,
        location=user_data.location,
        farm_size=user_data.farm_size
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": db_user.email})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=db_user.id,
        user_type=db_user.user_type
    )

@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        user_type=user.user_type
    )

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "user_type": current_user.user_type,
        "language_preference": current_user.language_preference,
        "location": current_user.location,
        "farm_size": current_user.farm_size
    }