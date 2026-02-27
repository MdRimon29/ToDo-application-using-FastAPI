from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker     # SQLAlchemy’s ORM converts Python classes into database tables.
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # Creates the database engine (a connection to Postgres).
SessionLocal = sessionmaker(autocommit=False, bind=engine, autoflush=False) 
Base = declarative_base()   # Logic to map Python objects → SQL rows

def get_db():   # This function is used by FastAPI’s dependency injection.
    db = SessionLocal() # open connection
    try:
        yield db    # yield pauses the function, returns a value, and later continues after yield. FastAPI uses it for dependency injection cleanup.
    finally:
        db.close()