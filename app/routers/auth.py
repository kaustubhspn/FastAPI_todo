from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    API endpoint for user login.

    Parameters:
    - user_credentials (OAuth2PasswordRequestForm): User credentials including username (email) and password.
    - db (Session): SQLAlchemy database session.

    Returns:
    - A dictionary containing the access token and its type.
    """

    # Retrieve user from database based on the provided email address
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        # Return HTTP 403 (Forbidden) if user is not found
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        # Return HTTP 403 (Forbidden) if the provided password is incorrect
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # Create a new access token for the user
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
