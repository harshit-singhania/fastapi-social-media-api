import time
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import models 
from database import get_db, engine
from sqlalchemy.orm import Session
import schemas 
from typing import List

app = FastAPI() 

models.Base.metadata.create_all(bind=engine) 

    

# index route
@app.get('/') 
def root(): 
    return {'message': 'welcome to the Posts API'} 

# connect to postgresql 
while True: 
    try: 
        conn = psycopg2.connect("dbname=fastapi_db user=postgres password=12345")
        cursor = conn.cursor()
        print('connected succesfully')
        break
    except Exception as error: 
        print('connection failed') 
        print(f'error: {error}')
        time.sleep(2)

# orm test method
# @app.get('/sqlalchemy/') 
# def test_posts(db: Session = Depends(get_db)): 
#     posts = db.query(models.Post).all()
#     return {'status': f'success {posts}'}
    
    
# get all of your posts 
@app.get('/post', response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)): 
    
    # RAW SQL 
    # cursor.execute("""SELECT * FROM public.posts""")
    # posts_ = cursor.fetchall()
    
    # ORM
    posts = db.query(models.Post).all()
    return posts

# creating posts 
@app.post('/create_post', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)): 
    
    # RAW SQL 
    # cursor.execute("""INSERT INTO posts (title, content) VALUE (%s, %s) RETURNING *""", ( post.title, post.content))
    # new_post = cursor.fetchone() 
    # conn.commit()
    
    # ORM 
    # print(**post.dict())
    new_post = models.Post(**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# # retrieving a single post
@app.get('/posts/{id}', response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)): 
    
    # RAW SQL
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone() 
    # conn.commit()
    # if not post: 
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f'post does not exist') 
    # return {'data': post}
    
    # ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='post not in db')
    return post


# # deleting a specific post
@app.delete('/posts/{id}') 
def delete_post(id: int, db: Session = Depends(get_db)): 
    
    # RAW SQL
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted = cursor.fetchone() 
    # conn.commit()
    # if deleted == None: 
    #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f'post does not exist')  
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    # ORM 
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='post not in db')
    else: 
        post.delete(synchronize_session=False)
    

# # updating a specific post 
@app.put('/posts/{id}', response_model=schemas.PostResponse)
def update_post(id: int, post:schemas.PostCreate, db: Session = Depends(get_db)): 
    
    # RAW SQL
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s RETURNING *""", 
    #                (post.title, post.content, post.published))
    # updated_post= cursor.fetchone() 
    # if update_post == None: 
    #     raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f'post does not exist')  
    # return {'data': update_post}
    
    # ORM 
    post_query = db.query(models.Post).filter(models.Post.id == id) 
    post = post_query.first() 
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='post not in db')
    else: 
        post_query.update(post.dict(), synchronize_session=False) 
        db.commit() 
        return post_query.first()