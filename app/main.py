from fastapi import Body, FastAPI, Response, status, HTTPException
from typing import Union 
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = FastAPI() 

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
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post does not exist') 
    return {'data': post}
    
#     post = find_post(id)
#     if post is None: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'404 error. post not found')
#     return {'data': post}
    
# # deleting a specific post
# @app.delete('/posts/{id}') 
# def delete_post(id: int): 
    
#     def delete(post_id): 
#         for post in my_posts: 
#             if post['id'] == post_id: 
#                 my_posts.remove(post)
#                 return post
#         return None 
    
#     post = delete(id)
#     if post is None: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'404 error. post not found')
#     return {'message': f'post {post["title"]} has been deleted'}

# # updating a specific post 
# @app.put('/posts/{id}')
# def update_post(id: int, post: Post): 
    
#     def update(post_id, post): 
#         for i, p in enumerate(my_posts): 
#             if p['id'] == post_id: 
#                 my_posts[i] = post.dict()
#                 my_posts[i]['id'] = post_id
#                 return my_posts[i]
#         return None 
    
#     post = update(id, post)
#     if post is None: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'404 error. post not found')
#     return {'data': my_posts}