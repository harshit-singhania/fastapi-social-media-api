from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from utils import hashing
import oauth2
import database 
import schemas 
import models 
from database import get_db

router = APIRouter(
    tags=['Authentication']
) 

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)): 
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first() 
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='wrong email or password') 
    if not hashing.verify(user_credentials.password, user.password) : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='wrong email or password') 
    
    # create token 
    access_token = oauth2.create_access_token(data={'user_id':user.id}) 
    return {'access_token': access_token, 'type': 'bearer_token'}
    
    