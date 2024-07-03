from typing import Optional
from pydantic import BaseModel, EmailStr, conint
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

class UserOut(BaseModel): 
    id: int 
    email: EmailStr 
    created_at: datetime
    class Config: 
        orm_mode = True

# we send data back to the user 

class PostResponse(PostBase): 
    id: int
    created_at : datetime
    owner_id: int 
    owner: UserOut
    
    class Config: 
        orm_mode = True
        
class UserCreate(BaseModel): 
    email: EmailStr
    password: str 
    class Config: 
        orm_mode = True 
        
class PostOut(PostBase): 
    Post: PostResponse
    votes: int 
        
class UserLogin(BaseModel): 
    email: EmailStr
    password: str
    
class Token(BaseModel): 
    access_token: str 
    token_type: str 

class TokenData(BaseModel): 
    id: Optional[str] = None 
    
from pydantic import PositiveInt

class Vote(BaseModel): 
    post_id: int 
    dir: PositiveInt