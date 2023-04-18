from .. import models, schemas
from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from .. import oauth2

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts

@router.get("/{id}")
def get_posts_id(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id, models.Post.owner_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} not found")
        
    return post

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the action")
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the action")
    
    post_query.update(update_post.dict(),synchronize_session=False)

    db.commit()

    return post_query.first()