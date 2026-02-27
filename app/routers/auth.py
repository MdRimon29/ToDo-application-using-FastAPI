from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import jwt
from datetime import timedelta, timezone, datetime
from .. schemas import UserRequest, Token
from .. models import User
from .. database import get_db
from .. utils import get_password_hash, verify_password
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY  = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_EXPIRE_TOKEN_MINUTES = 30

db_dependency = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return False
    if not verify_password(password, user.hash_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role:str, expire_delta:timedelta):
    payload = {'sub':username, 'id':user_id, 'role':role}
    expires = datetime.now(timezone.utc)+expire_delta
    payload["exp"] = expires
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username:str = payload.get('sub')
        user_id:int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username': username, 'user_id': user_id, 'user_role':user_role}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')



#### User create using hash password
@router.post("/post_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequest):
    hashed_password = get_password_hash(user_request.hash_password)
    user_request.hash_password = hashed_password
    create_one_user = User(**user_request.model_dump())
    db.add(create_one_user)
    db.commit()
    return {"Message": "User has been created successfully."}



#### Autheticate user using username and password
@router.post("/token", response_model=Token)
async def login_for_access_token(db: db_dependency, form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed authentication"
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=ACCESS_EXPIRE_TOKEN_MINUTES))
    return {'access_token':token, 'token_type':'bearer'}


# model_dump() → converts Pydantic object → dict.
# **dict → unpacks dict into keyword arguments for SQLAlchemy model.
# create_one_user → now a SQLAlchemy object that can be db.add() and db.commit().