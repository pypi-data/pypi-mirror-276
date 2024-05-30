from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fast_auth.auth.models import User, UserInDB
from fast_auth.auth.db import db
from fast_auth.auth.utils import verify_password, get_password_hash, create_access_token, oauth2_scheme
from datetime import timedelta

auth_router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class UserInResponse(BaseModel):
    email: str

@auth_router.post("/signup", response_model=UserInResponse)
async def create_user(user: User):
    user_in_db = await db.get_user(user.email)
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(email=user.email, hashed_password=hashed_password)
    await db.create_user(user_in_db)
    return UserInResponse(email=user.email)

@auth_router.post("/login", response_model=Token)
async def login(user: User):
    user_in_db = await db.get_user(user.email)
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_password(user.password, user_in_db['hashed_password']):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@auth_router.post("/reset-password")
async def reset_password(email: str, new_password: str):
    user_in_db = await db.get_user(email)
    if not user_in_db:
        raise HTTPException(status_code=400, detail="User not found")
    hashed_password = get_password_hash(new_password)
    await db.users_collection.update_one({"email": email}, {"$set": {"hashed_password": hashed_password}})
    return {"msg": "Password updated successfully"}

@auth_router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    await db.add_token_to_blacklist(token)
    return {"msg": "Successfully logged out"}
