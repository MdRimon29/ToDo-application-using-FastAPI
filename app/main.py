from fastapi import FastAPI
from . database import engine, Base
from . routers import auth, todo, admin, user

Base.metadata.create_all(bind=engine) # this line create database

app = FastAPI()
    
app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(user.router)