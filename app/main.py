from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import desc
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# while True:
#     try:
#         conn = psycopg2.connect(host = "localhost",dbname = "fastapi", user = "postgres", 
#                             password = "test123", cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print("Database connected successfully!")
#         break
#     except Exception as error:
#         print("Database connection error ", error)
#         time.sleep(2)

my_posts =[{"title": "Helllooo", "content": "I love pizza", "id":1},{"title": "Hello Nada", "content":"How are you?", "id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    post = db.query(models.Post)
    print(post)
    return {"data" : "successfull"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cur.execute("select * from posts;")
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def new_post(post: Post, db: Session = Depends(get_db)):

    # cur.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
    #             (post.title, post.content, post.published))
    
    # new_post = cur.fetchone()

    # conn.commit()

    # print(post.dict())
    new_post = models.Post(**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post(db: Session = Depends(get_db)):
    
    # cur.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT 1;")
    # post = cur.fetchone()

    post = db.query(models.Post).order_by(desc(models.Post.id)).limit(1).first()

    return {"details" : post}


@app.get("/posts/{id}")
def get_post(id : int, db: Session = Depends(get_db)):

    # cur.execute("SELECT * FROM posts WHERE id = %s;",(str(id)))
    # post = cur.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} was not found!")
    
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db)):

    # cur.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (str(id)))
        
    # post = cur.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")
    
    post.delete(synchronize_session=False)
    db.commit()
   
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
   
    # cur.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;", 
    #              (post.title, post.content, post.published, (str(id))))
        
    # post_dict = cur.fetchone()
    
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} was not found!")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    
    return {"detail" : post_query.first()}