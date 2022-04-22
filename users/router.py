from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import db
from . import schema
from . import services
from . import validation

api_router = APIRouter(tags = ['Users'])

@api_router.post('/user/', status_code=status.HTTP_201_CREATED, response_model=schema.User)
async def create_user_registration(user_in: schema.UserCreate, db_session: Session = Depends(db.get_db_session)):
    user = await validation.verify_email_exist(user_in.email, db_session)
    if user:
        raise HTTPException(
            status_code=400, detail="The user with this email already exists in the system.")
    new_user = await services.new_user_register(user_in, db_session)
    return new_user

@api_router.get('/user/', response_model = List[schema.User])
async def get_all_users(db_session: Session = Depends(db.get_db_session)):
    return await services.all_users(db_session)

@api_router.get('/user/{user_id}', response_model = schema.User)
async def get_user_by_id(user_id: int, db_session: Session = Depends(db.get_db_session)):
    return await services.get_user_by_id(user_id, db_session)

@api_router.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: int, db_session: Session = Depends(db.get_db_session)):
    user = await services.get_user_by_id(user_id, db_session)
    if not user:
        raise HTTPException(status_code=404, detail = "You have provided invalid user id")
    
    return await services.delete_user_by_id(user_id, db_session)

@api_router.put('/user/{user_id}', status_code = status.HTTP_201_CREATED)
async def update_user(user_id: int, user: schema.UserUpdate, db_session: Session = Depends(db.get_db_session)):
    new_user = await services.update_user(user_id, user, db_session)
    if not new_user:
        raise HTTPException(status_code=404, detail = "You have provided invalid user id")
    return new_user