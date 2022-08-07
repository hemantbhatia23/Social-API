from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut 

    class Config:  # will tell pydantic model to read data even if its not a dict
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    likes: int
    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Like(BaseModel):
    post_id: int
    dir: conint(le=1)
# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool