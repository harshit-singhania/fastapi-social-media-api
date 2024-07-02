# path operations for users 
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models 
import schemas 
from database import get_db
from utils import hashing 
from typing import Optional, List
from sqlalchemy.orm import Session 

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

# create user account   
@router.post('/', 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, 
                db: Session = Depends(get_db)): 
    # check if user exists 
    user_exists = db.query(models.User).filter(models.User.email == user.email).first() 
    if user_exists: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user already exists')
    
    hashed_pwd = hashing.password_hash(user.password) # hashing the password
    user.password = hashed_pwd
    new_user = models.User(**user.dict()) 
    
    db.add(new_user) 
    db.commit() 
    db.refresh(new_user) 
    return new_user

# getting user by id
@router.get('/{id}', 
            response_model=schemas.UserOut) 
def get_user(id: int, db: Session = Depends(get_db)): 
    user = db.query(models.User).filter(models.User.id == id).first() 
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user not found') 
    return user 