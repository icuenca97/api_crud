from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

app = FastAPI()

posts = []
id = 0

class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text #tipo de dato simil sting, pero largo
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False

@app.get('/')
def read_root():
    return {'welcome': 'Welcome to my API'}

@app.get('/posts')
def get_posts():
    return posts

@app.post('/posts')
def save_posts(post: Post):
    global id
    id += 1
    post.id = str(id)
    posts.append(post.dict())
    return posts[-1]

@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=404, detail='Post not found')

@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post['id'] == post_id:
            posts.pop(index)
            return {'message': 'Post has been deleted successfully'}
    raise HTTPException(status_code=404, detail='Post not found')

@app.put('/posts/{post_id}')
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post['id'] == post_id:
            posts[index]['title'] = updatedPost.title
            posts[index]['author'] = updatedPost.author
            posts[index]['content'] = updatedPost.content
            return {'message': 'Post has been updated successfully'}
    raise HTTPException(status_code=404, detail='Post not found')
