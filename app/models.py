from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"

    id = mapped_column(Integer,primary_key=True, nullable=False)
    title = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    created_at = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    due_at = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    owner_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE",),nullable=False)
    owner = relationship("User")



class User(Base):
    __tablename__ = "users"
    name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False,unique=True)
    password = mapped_column(String, nullable=False)
    id = mapped_column(Integer, primary_key=True, nullable=False)
    created_at = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
