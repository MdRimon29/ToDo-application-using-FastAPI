from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from ..database import get_db
from ..models import Todo
from ..schemas import TodoRequest
from sqlalchemy.orm import Session
from .auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


db_dependecy = Annotated[Session, Depends(get_db)]  # Here depends is dependency injection
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/todo')
async def read_all(db: db_dependecy, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    elif user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not an admin")
    all_todo = db.query(Todo).all()
    return all_todo


@router.delete('/todo/{todo_id}')
async def delete_todo_by_id(db: db_dependecy, user: user_dependency, todo_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    elif user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not an admin")
    todo_by_id = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_by_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task is not found")
    
    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()
    return {"Message": "This todo is is deleted by admin"}