# path operations for posts 

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models 
import schemas 
from database import get_db
from utils import hashing 
from typing import Optional, List
from sqlalchemy.orm import Session 
from sqlalchemy import func
import oauth2

router = APIRouter(
    prefix='/posts', 
    tags=['Posts']
)

# get all of your posts 
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user), 
              search: Optional[str] = None,
              limit: int = 10, skip: int = 0): 
    
    # RAW SQL 
    # cursor.execute("""SELECT * FROM public.posts""")
    # posts_ = cursor.fetchall()
    
    # ORM
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post, 
                       func.count(models.Vote.post_id).label('votes').join(
        models.Vote, 
        models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all() 
       
    return results

# creating posts 
@router.post('/create_post', 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)): 
    
    # RAW SQL 
    # cursor.execute("""INSERT INTO posts (title, content) VALUE (%s, %s) RETURNING *""", ( post.title, post.content))
    # new_post = cursor.fetchone() 
    # conn.commit()
    
    # ORM 
    # print(**post.dict())

    new_post = models.Post(
        owner_id=current_user.id, **post.dict()
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# # retrieving a single post
@router.get('/{id}', 
            response_model=schemas.PostOut)
def get_post(id: int, 
             db: Session = Depends(get_db), 
             user_id: int = Depends(oauth2.get_current_user)):  
    
    # RAW SQL
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone() 
    # conn.commit()
    # if not post: 
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f'post does not exist') 
    # return {'data': post}
    
    # ORM
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, 
                    func.count(models.Vote.post_id).label('votes')).join(models.Vote, 
                    models.Vote.post_id == models.Post.id, 
                    isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='post not in db')
    return post


# # deleting a specific post
@router.delete('/{id}', 
               status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id: int, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)): 
    
    # RAW SQL
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted = cursor.fetchone() 
    # conn.commit()
    # if deleted == None: 
    #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f'post does not exist')  
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    # ORM 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='post not in db')
    
    if post.owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not authorised to delete someone elses post')
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# # updating a specific post 
@router.put('/{id}', 
            response_model=schemas.PostResponse)
def update_post(id: int, 
                updated_post:schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)): 
    
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
    if post.owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='illegal action') 
    
     
    post_query.update(post.dict(), synchronize_session=False) 
    db.commit() 
    return post_query.first()

