from fastapi import Body, FastAPI, Response, status, HTTPException
from typing import Union 
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from . import models 
from .database import SessionLocal, engine

app = FastAPI() 

models.Base.metadata.create_all(bind=engine) 

def get_db(): 
    db = SessionLocal() 
    try: 
        yield db 
    finally: 
        db.close()
        
class Post(BaseModel): 
    title: str 
    content: str 
    published: bool = True

# index route
@app.get('/') 
def root(): 
    return {'message': 'welcome to the Posts API'} 

# connect to postgresql 
try: 
    conn = psycopg2.connect("dbname=fastapi_db user=postgres password=12345")
    cursor = conn.cursor()
    print('connected succesfully')
except Exception as error: 
    print('connection failed') 
    print(f'error: {error}')
    
# get all of your posts 
@app.get('/post')
def get_posts(): 
    cursor.execute("""SELECT * FROM public.posts""")
    posts_ = cursor.fetchall()
    return {'data': posts_}

# creating posts 
@app.post('/create_post', status_code=status.HTTP_201_CREATED)
def create_posts(post): 
    cursor.execute("""INSERT INTO posts (title, content) VALUE (%s, %s) RETURNING *""", ( post.title, post.content))
    new_post = cursor.fetchone() 
    conn.commit()
    return {'data': f'post created {new_post}'}


# # retrieving a single post
@app.get('/posts/{id}')
def get_post(id: int): 
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone() 
    conn.commit()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post does not exist') 
    return {'data': post}
    
    
# # deleting a specific post
@app.delete('/posts/{id}') 
def delete_post(id: int): 
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted = cursor.fetchone() 
    conn.commit()
    if deleted == None: 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post does not exist')  
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

# # updating a specific post 
@app.put('/posts/{id}')
def update_post(id: int, post): 
    
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s RETURNING *""", 
                   (post.title, post.content, post.published))
    updated_post= cursor.fetchone() 
    if update_post == None: 
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post does not exist')  
    return {'data': update_post}