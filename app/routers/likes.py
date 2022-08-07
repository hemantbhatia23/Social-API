from email.policy import HTTP
from multiprocessing import synchronize
from fastapi import Body, FastAPI, APIRouter,Depends, Response, status, HTTPException
import models, schemas, utils
from sqlalchemy.orm import Session
from database import  get_db
from typing import Optional, List
from . import oauth2

router = APIRouter(
    prefix="/like",
    tags = ['Like']
)

@router.post('/', status_code = status.HTTP_201_CREATED)
def like(like: schemas.Like,db: Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Post with {like.post_id} doesn't exist")    

    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)
    found_like = like_query.first()
    if like.dir == 1:
        if found_like:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"User {current_user.id} has already liked post {like.post_id}")    
        else:
            new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
            db.add(new_like)
            db.commit()
        return {"message":"Succesfully liked the post"}
    else:
        if not found_like:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Vote doesn't exist")
        else:
            like_query.delete(synchronize_session = False)
            db.commit()
        return {"message":"Succesfully removed like"}
