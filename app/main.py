import time
from fastapi import FastAPI
# import psycopg2
import models 
from database import engine
from routers import post, user, auth
from pydantic import BaseSettings 
from config import Settings 
from routers import vote 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() 

origins = ['*']

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=['*'], 
    allow_headers=['*'], 
)

# models.Base.metadata.create_all(bind=engine) 

app.include_router(post.router) 
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# index route 
@app.get('/') 
def root(): 
    return {'message': 'welcome to the Posts API'} 

# while True: 
#     try: 
#         conn = psycopg2.connect("dbname=fastapi_db user=postgres password=12345")
#         cursor = conn.cursor()
#         print('connected succesfully')
#         break
#     except Exception as error: 
#         print('connection failed') 
#         print(f'error: {error}')
#         time.sleep(2)

# orm test method
# @app.get('/sqlalchemy/') 
# def test_posts(db: Session = Depends(get_db)): 
#     posts = db.query(models.Post).all()
#     return {'status': f'success {posts}'}


    
