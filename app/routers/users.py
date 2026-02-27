from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from ..database import get_db
from ..models import Todo, User
from ..schemas import Password_Change
from sqlalchemy.orm import Session
from .auth import get_current_user
from .. utils import verify_password, get_password_hash


router = APIRouter(
    prefix='/user',
    tags=['User']
)


db_dependecy = Annotated[Session, Depends(get_db)]  # Here depends is dependency injection
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/")
async def all_users(db: db_dependecy, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    all_user = db.query(User).filter(User.id == user.get('user_id')).first()
    return db.query(User).filter(User.id == user.get('user_id')).first()


@router.put('/password')
async def change_password(db: db_dependecy, user: user_dependency, password_change: Password_Change):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    user_model = db.query(User).filter(User.id == user.get('user_id')).first()

    if not verify_password(password_change.password, user_model.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    user_model.hash_password = get_password_hash(password_change.new_password)
    db.add(user_model)
    db.commit()
    return {"Message": "Password has been changed successfully."}