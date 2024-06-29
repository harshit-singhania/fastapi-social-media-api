from fastapi import Body, FastAPI, Response, status, HTTPException
from typing import Union 
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI() 

# posts schema 
class Post(BaseModel): 
    title: str 
    content: str 
    published: bool = True 
    rating: Optional[int] = None

# dummy route #1 
@app.get('/') 
def root(): 
    return {'message': 'welcome to my api'} 

# get all of your posts 
@app.get('/posts')
def get_posts(): 
    return {'data': my_posts}

# dummy post database 
my_posts = [
    {
        'title': 'example post 1', 
        'content': 'example post #1',
        'published': True,
        'rating': 4,
        'id': 1 
    },
    {
        'title': 'example post 2',
        'content': 'example post #2',
        'published': True,
        'rating': 5,
        'id': 2
    }, 
    {
        'title': 'example post 3',
        'content': 'example post #3',
        'published': True, 
        'rating': 3,
        'id': 3
    }
]

# creating posts 
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post:Post): 
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {'data': my_posts}

# retrieving a single post
@app.get('/posts/{id}')
def get_post(id: int, response: Response): 
    
    def find_post(post_id): 
        for post in my_posts: 
            if post['id'] == post_id: 
                return post
        return None
    
    post = find_post(id)
    if post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'404 error. post not found')
    return {'data': post}
    
# deleting a specific post
@app.delete('/posts/{id}') 
def delete_post(id: int): 
    
    def delete(post_id): 
        for post in my_posts: 
            if post['id'] == post_id: 
                my_posts.remove(post)
                return post
        return None 
    
    post = delete(id)
    if post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'404 error. post not found')
    return {'message': f'post {post["title"]} has been deleted'}

# updating a specific post 
@app.put('/posts/{id}')
def update_post(id: int, post: Post): 
    
    def update(post_id, post): 
        for i, p in enumerate(my_posts): 
            if p['id'] == post_id: 
                my_posts[i] = post.dict()
                my_posts[i]['id'] = post_id
                return my_posts[i]
        return None 
    
    post = update(id, post)
    if post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'404 error. post not found')
    return {'data': my_posts}