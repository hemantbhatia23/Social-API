from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    

while True:
    try:
        conn = psycopg2.connect(host = 'hostname', database = 'db_name',
            user = 'username', password = 'password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "Welcome"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts} 

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) values (%s, %s, %s) RETURNING *""", 
                        (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data" : new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, 
                        (str(id)))
    post = cursor.fetchone()
    print(post)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail = f"post with {id} not found")
    return {"post-detail" : post}

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"data" : post}


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #delete post
    # find index in array of required id
    # my_posts.pop(index)
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"{id} doesnt exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
            (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"{id} doesnt exist")

    return {"message": updated_post}
