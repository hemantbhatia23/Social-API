from email.policy import HTTP
from fastapi import Body, FastAPI, APIRouter,Depends, Response, status, HTTPException
import models, schemas, utils
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import  get_db
from typing import Optional, List
from . import oauth2

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db:  Session = Depends(get_db),current_user :int  = Depends(oauth2.get_current_user),
    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    
    results = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.Post.id, isouter = True).group_by(models.Post.id)
    results = results.filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db:  Session = Depends(get_db), current_user :int  = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) values (%s, %s, %s) RETURNING *""", 
    #                     (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    #new_post = models.Post(title = post.title, content = post.content, published = post.published)
    #post_dict = post.dict()
    #post_dict["owner_id"] = current_user.id
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db:  Session = Depends(get_db), current_user :int  = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, 
    #                     (str(id)))
    # post = cursor.fetchone()
    # print(post)
    post = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.Post.id, isouter = True).group_by(models.Post.id)
    post = post.filter(models.Post.id == id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail = f"post with id {id} not found")
    return  post

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"data" : post}


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user :int  = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"{id} doesnt exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session= False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post_new: schemas.PostCreate, db: Session = Depends(get_db), current_user :int  = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #         (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"{id} doesnt exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail="Not authorized to perform requested action")

    post_query.update(post_new.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()