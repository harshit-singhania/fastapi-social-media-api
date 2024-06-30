from .database import Base
from sqlalchemy import Boolean, Column, Integer, String

# create the post table in ORM
class Post(Base): 
    __tablename__ = 'posts' 
    id = Column(Integer, primary_key=True, nullable=False) 
    title = Column(String, nullable=False) 
    content = Column(String, nullable=False) 
    published = Column(Boolean, nullable=True, default=True) 
    
    