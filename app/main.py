import time
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import models 
from database import get_db, engine
from sqlalchemy.orm import Session
import schemas 
from typing import List
from utils import hashing
from routers import post, user 
app = FastAPI() 

models.Base.metadata.create_all(bind=engine) 

app.include_router(post.router) 
app.include_router(user.router)
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


    
