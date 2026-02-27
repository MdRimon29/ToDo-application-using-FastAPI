# Defines database tables using SQLAlchemy ORM.

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    hash_password = Column(String)
    is_active = Column(String, default=True)
    role = Column(String)


class Todo(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index= True)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))   # syntax is -> "table_name.column_name"
