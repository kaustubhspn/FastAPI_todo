from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_port}:{settings.database_password}@{settings.database_hostname}/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
