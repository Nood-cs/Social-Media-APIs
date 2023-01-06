from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts =[{"title": "Heppy new year", "content": "2023", "id":1},{"title": "Hello Nada", "content":"How are you?", "id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/createpost")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new post": f"{payload['Title']}, {payload['Content']}"}


@app.post("/posts")
def new_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1,10000000)
    my_posts.append(post_dict)
    return {"new post": post_dict}


@app.get("/posts/{id}")
def get_post(id):
    print(type(id))
    post = find_post(int(id))
    print(post)
    return {"post_details": post['title']}