from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from sqlalchemy.util import deprecated

from database import database
from sqlalchemy import text
import os


router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY="super-duper"


class UserRegistration(BaseModel):
    username: str
    password: str
    role: str   # monster or human

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

"""
class AuthRequest(BaseModel):
    username: str
    password: str
"""


@router.post("/register")
async def register_user(user: UserRegistration):
    print("starting regestration process...")
    if user.role not in ["human", "monster"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    query = text("SELECT * FROM users WHERE usernmae = :username")
    existing_user = await database.fetch_one(query=query, values={"username": user.username})

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(user.password)
    insert_query = text("""
                        INSERT INTO users (username, password, role)
                        VALUES (:username, :password, :role)
                        """)

    await database.execute(query=insert_query, values={
                           "username": user.username,
                           "password": hashed_password,
                           "role": user.role
    })

    return {"message": "User registered successfully"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = text("SELECT * FROM users WHERE username = :username")
    user = await database.fetch_one(query=query, values={"username": form_data.username})

    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
            data={"sub": user["username"], "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return {"username": username, "role": role}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
