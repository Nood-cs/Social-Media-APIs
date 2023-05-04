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
    print(posts)
    return {"data": posts}

# @app.post("/createpost")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new post": f"{payload['Title']}, {payload['Content']}"}
# title str, content str


@app.post("/createpost")
def createpost(new_post: Post):
    print(new_post)
    post_dict = new_post.dict()
    print(post_dict)
    return {"data": post_dict}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def new_post(post: Post):
    new_post = post.dict()
    new_post['id'] = randrange(0, 1000000)
    my_posts.append(new_post)
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)- 1]
    print(post)
    return {"details" : post}

@app.get("/posts/{id}")
def get_post(id : int):
    post = find_post(id)
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} was not found!")
    print(post)
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):

    index = find_post_index(id)
    print(index)
    if index is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id {id} was not found!")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
   
   index = find_post_index(id)

   if index == None:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id {id} was not found!")
   
   post_dict = post.dict() # has not id
   post_dict['id'] = id
   my_posts[index] = post_dict
   return {"detail" : post_dict}