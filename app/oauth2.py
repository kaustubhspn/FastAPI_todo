# Importing the required modules and packages.
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, database, models
from .config import settings

# Creating an instance of OAuth2PasswordBearer class for token authentication.
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Retrieving the required settings from the config.
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)

# Function to generate the access token.
def create_access_token(data: dict) -> str:
    """
    This function generates an access token for the given data.
    Args:
    data(dict): Dictionary containing the data to be encoded in the token.

    Returns:
    str: Encoded access token string.
    """

    # Creating a copy of the data to be encoded.
    to_encode = data.copy()

    # Setting the expiry time of the token.
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Encoding the token using the given secret key and algorithm.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# Function to verify the access token.
def verify_access_token(token: str, credentials_exception: HTTPException) -> schemas.TokenData:
    """
    This function verifies the given access token and returns the user ID from the token.
    Args:
    token(str): Access token to be verified.
    credentials_exception(HTTPException): Exception to be raised if token is invalid.

    Returns:
    TokenData: TokenData object containing the user ID from the token.
    """

    try:
        # Decoding the token to retrieve the payload.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Retrieving the user ID from the payload.
        id: str = payload.get("user_id")

        # Raising an exception if user ID is not present in the payload.
        if not id:
            raise credentials_exception

        # Creating a TokenData object with the user ID from the token.
        token_data = schemas.TokenData(id=id)

    except JWTError:
        # Raising an exception if the token is invalid.
        raise credentials_exception
    
    return token_data

# Function to get the current user from the access token.
def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(database.get_db)) -> models.User:
    """
    This function retrieves the current user from the access token.
    Args:
    token(str): Access token to be verified.
    db(Session): Database session dependency.

    Returns:
    User: User object representing the current user.
    """

    # Creating an exception to be raised if credentials are invalid.
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    # Verifying the access token and retrieving the user ID.
    token = verify_access_token(token, credentials_exception)

    # Querying the database to retrieve the user with the given ID.
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
