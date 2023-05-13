from typing import List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import desc
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.get("/")
def root():
    return {"message": "Welcome to my API"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

