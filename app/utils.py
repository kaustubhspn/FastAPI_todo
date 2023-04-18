# Importing the required modules.
from passlib.context import CryptContext

# Creating an instance of CryptContext class with bcrypt scheme and auto-deprecation.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to generate the hash of the password.
def hash(password: str) -> str:
    """
    This function returns the hash of the given password using bcrypt algorithm.
    Args:
    password(str): Plain password to be hashed.

    Returns:
    str: Hashed password string.
    """

    # Using the hash() method of CryptContext to generate the hash.
    return pwd_context.hash(password)

# Function to verify the given password with the hashed password.
def verify(plain_password: str, hashed_password: str) -> bool:
    """
    This function verifies the given plain password with the hashed password using bcrypt algorithm.
    Args:
    plain_password(str): Plain password to be verified.
    hashed_password(str): Hashed password string.

    Returns:
    bool: True if the given password is valid, False otherwise.
    """

    # Using the verify() method of CryptContext to compare the plain password with hashed password.
    return pwd_context.verify(plain_password, hashed_password)