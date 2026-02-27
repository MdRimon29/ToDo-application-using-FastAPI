from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from ..database import get_db
from ..models import Todo
from ..schemas import TodoRequest
from sqlalchemy.orm import Session
from .auth import get_current_user


db_dependecy = Annotated[Session, Depends(get_db)]  # Here depends is dependency injection
user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter()


@router.get("/")
def welcome():
    return {"Hello":"Welcome to this to-do application"}



##### Get all todo 
@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(db : db_dependecy, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return db.query(Todo).filter(Todo.owner_id==user.get("user_id")).all()



##### Get todo by id
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(db: db_dependecy,user: user_dependency, todo_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    todo_by_id = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('user_id')).first()
    if todo_by_id is not None:
        return todo_by_id
    raise HTTPException(status_code=404, detail="Detail not found")



#### Post a todo task
@router.post("/post_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependecy, user:user_dependency, todo_request : TodoRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    todo_model = Todo(**todo_request.model_dump(), owner_id=user.get("user_id"))
    db.add(todo_model)
    db.commit()
    return {"Message": "TODO created successfully"}



#### Update/Put a todo 
@router.put("/put_todo/{todo_id}")
async def update_todo(db: db_dependecy,
                      user:user_dependency,
                      todo_request: TodoRequest,
                      todo_id : int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    todo_by_id = db.query(Todo).filter(Todo.id == todo_id).filter(user.get("user_id")==Todo.owner_id).first()
    if todo_by_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    todo_by_id.title = todo_request.title
    todo_by_id.priority = todo_request.priority
    todo_by_id.description = todo_request.description
    todo_by_id.completed = todo_request.completed

    db.add(todo_by_id)
    db.commit()
    return {"Message": "Database updated for this user."}



#### Todo delete by its id
@router.delete("/todo/{todo_id}")
async def delete_todo(db: db_dependecy,
                      user : user_dependency,
                      todo_id: int=Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    todo_by_id = db.query(Todo).filter(todo_id == Todo.id).filter(user.get("user_id")==Todo.owner_id).first()
    if todo_by_id is None:
        raise HTTPException(status_code=402, detail = "User not found")
    db.query(Todo).filter(todo_id == Todo.id).delete()
    db.commit()
    return {"Message": "Todo is deleted by its id."}