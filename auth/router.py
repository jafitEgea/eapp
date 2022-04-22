from typing import Any
from fastapi import APIRouter, Depends, status, HTTPException
import fastapi
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.security import create_access_token
from database import db
from users.services import authenticate

api_router = APIRouter(tags=["Auth"])

@api_router.post("/login")
def login(db: Session= Depends(db.get_db_session), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = authenticate(email = form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    return {
        "access_token": create_access_token(sub=user.email),
        "token_type": "Bearer",
    }