from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schema import UserCreate, UserLogin
from app.services.auth_services import signup_user, login_user

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate):
    return signup_user(user)

@router.post("/login")
def login(user: UserLogin):
    return login_user(user)