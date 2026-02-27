from fastapi import FastAPI
from . database import engine, Base
from . routers import auth, todo, admin, users

Base.metadata.create_all(bind=engine) # this line create database

app = FastAPI()
    
app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(users.router)