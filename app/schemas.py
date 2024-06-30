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
    title: str  
    created_at : datetime
    class Config: 
        orm_mode = True 
        
def UserCreate(BaseModel): 
    email: EmailStr
    password: str 
    class Config: 
        orm_mode = True 
        
class UserOut(BaseModel): 
    id: int 
    email: EmailStr 
    class Config: 
        orm_mode = True