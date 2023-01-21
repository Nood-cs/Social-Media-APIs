from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
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


def find_post_id(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


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


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def new_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1,10000000)
    my_posts.append(post_dict)
    return {"new post": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)- 1]
    print(post)
    return {"details" : post}

@app.get("/posts/{id}")
def get_post(id : int):
    
    post = find_post(id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id}, was not found!')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message' : f'post with id: {id}, was not found!'}    
    print(post)
    
    return {"post_details": post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    p = find_post_id(id)
    
    if p is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id}, may be deleted already!')
    
    print(p)
    my_posts.pop(p)
    return Response(status_code=status.HTTP_204_NO_CONTENT)