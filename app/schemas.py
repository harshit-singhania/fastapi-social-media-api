from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
# user sends data to us 

class PostBase(BaseModel): 
    title: str 
    content: str 
    publishes: bool = True 
    class Config: 
        orm_mode = True

class PostCreate(PostBase): 
    pass 

# we send data back to the user 

class PostResponse(PostBase): 
    id: int
    created_at : datetime
    owner_id: int 
        
def UserCreate(BaseModel): 
    email: EmailStr
    password: str 
    class Config: 
        orm_mode = True 
        
class UserOut(BaseModel): 
    id: int 
    email: EmailStr 
    created_at: datetime
    class Config: 
        orm_mode = True
        
class UserLogin(BaseModel): 
    email: EmailStr
    password: str
    
class Token(BaseModel): 
    access_token: str 
    token_type: str 

class TokenData(BaseModel): 
    id: Optional[str] = None 