from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Define the database URL using the values from the settings file
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_port}:{settings.database_password}@{settings.database_hostname}/fastapi'


# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

# Create a session factory using the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function to get a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
