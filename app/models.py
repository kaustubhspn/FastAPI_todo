from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

"""

Note that this code defines two SQLAlchemy models, Post and User, 
with columns and relationships defined using SQLAlchemy's ORM. 

The Base class is a helper class provided by SQLAlchemy to be used 
as the base for all declarative models.

The mapped_column function is used to create mapped columns with 
their data type and other options. 

The relationship function is used to define a relationship between 
two tables.

"""

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"

    # Column definitions
    id = mapped_column(Integer, primary_key=True, nullable=False)
    title = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    created_at = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    due_at = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    owner_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Relationship with User
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    
    # Column definitions
    name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False, unique=True)
    password = mapped_column(String, nullable=False)
    id = mapped_column(Integer, primary_key=True, nullable=False)
    created_at = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
