from pydantic import BaseModel 
from datetime import datetime
# user sends data to us 

class PostBase(BaseModel): 
    title: str 
    content: str 
    publishes: bool = True 

class PostCreate(PostBase): 
    pass 

# we send data back to the user 

class PostResponse(BaseModel): 
    title: str 
    content: str 
    published: bool  
    created_at : datetime
    class Config: 
        orm_mode = True 