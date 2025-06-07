from app.schemas.user_schema import UserCreate, UserLogin
from app.models.user_model import User
from sqlalchemy.orm import Session
import bcrypt

def signup_user(user: UserCreate):
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    # store user in DB
    return {"msg": "User created"}

def login_user(user: UserLogin):
    # validate user credentials
    return {"msg": "Login successful"}
