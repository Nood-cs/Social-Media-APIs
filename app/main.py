from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host = "127.0.0.1",dbname = "fastapi", user = "postgres", 
                            password = "test123", cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Database connected successfully!")
        break
    except Exception as error:
        print("Database connection error ", error)
        time.sleep(2)

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

@app.get("/posts")
def get_posts():
    cur.execute("select * from posts;")
    posts = cur.fetchall()
    
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def new_post(post: Post):

    cur.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
                (post.title, post.content, post.published))
    
    new_post = cur.fetchone()

    conn.commit()

    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    
    cur.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT 1;")
    post = cur.fetchone()

    return {"details" : post}


@app.get("/posts/{id}")
def get_post(id : int):

    cur.execute("SELECT * FROM posts WHERE id = %s;",(str(id)))
    post = cur.fetchone()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} was not found!")
    
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):

    cur.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (str(id)))
        
    post = cur.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")
   
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
   
    cur.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;", 
                 (post.title, post.content, post.published, (str(id))))
        
    post_dict = cur.fetchone()
    
    conn.commit()
    
    if post_dict is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} was not found!")
    
    return {"detail" : post_dict}