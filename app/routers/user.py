from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user with the provided user data.
    """
    # Hash the user's password before storing in the database
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Create a new user object with the provided data
    new_user = models.User(**user.dict())

    # Add the new user to the database and commit the transaction
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the new user object
    return new_user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID.
    """
    # Retrieve the user with the given ID
    user = db.query(models.User).filter(models.User.id == id).first()

    # If the user is not found, raise a 404 error
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")

    # Return the user object
    return user
