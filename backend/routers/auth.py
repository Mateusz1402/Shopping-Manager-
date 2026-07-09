from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from tables.tables_definition import Users
from schemas import AuthSchema
from passlib.context import CryptContext
import jwt
import datetime

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "YOUR_SUPER_SECRET_KEY"

@router.post("/register")
def register(data: AuthSchema, db: Session = Depends(get_db)):
    if db.query(Users).filter(Users.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    is_first_user = db.query(Users).count() == 0
    role = "admin" if is_first_user else "guest"

    new_user = Users(
        username = data.username,
        password = pwd_context.hash(data.password),
        role = role
    )

    db.add(new_user)
    db.commit()
    return {
        "message" : "New user successfully added!"
    }

@router.post("/login")
def login(data: AuthSchema, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == data.username).first()
    if not user or not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    payload = {
        "sub" : user.username,
        "role" : user.role, 
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {
        "token" : token,
        "role" : user.role,
        "username" : user.username
    }
