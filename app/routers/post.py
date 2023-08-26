from typing import List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):
    # cur.execute("select * from posts;")
    # posts = cur.fetchall()
    print(curr_user.email)

    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):

    # cur.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
    #             (post.title, post.content, post.published))
    
    # new_post = cur.fetchone()

    # conn.commit()

    # print(post.dict())
    print(curr_user.email)

    new_post = models.Post(**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):
    
    # cur.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT 1;")
    # post = cur.fetchone()
    print(curr_user.email)

    post = db.query(models.Post).order_by(desc(models.Post.id)).limit(1).first()

    return post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id : int, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):

    # cur.execute("SELECT * FROM posts WHERE id = %s;",(str(id)))
    # post = cur.fetchone()
    print(curr_user.email)

    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} was not found!")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):

    # cur.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (str(id)))
        
    # post = cur.fetchone()
    # conn.commit()
    print(curr_user.email)

    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")
    
    post.delete(synchronize_session=False)
    db.commit()
   
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):
   
    # cur.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;", 
    #              (post.title, post.content, post.published, (str(id))))
        
    # post_dict = cur.fetchone()
    
    # conn.commit()

    print(curr_user.email)
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} was not found!")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    
    return post_query.first()
