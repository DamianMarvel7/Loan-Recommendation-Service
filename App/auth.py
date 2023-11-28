from fastapi import APIRouter, Depends, status, HTTPException
import json
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from Utility.utils import  encode_token, decode_token, hash_password,verify_password
    

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str


router = APIRouter()


json_userfilename = "user.json"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def read_account_data():
    with open(json_userfilename, "r") as read_file:
        data = json.load(read_file)
    return data

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_token(token)
    users_db = read_account_data()
    
    user = get_user(users_db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    users_db = read_account_data()

    user_dict = users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = encode_token(user.username)
    return {"access_token": token,"username":form_data.username, "token_type": "bearer"}


class UserRegistration(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register_user(user: UserRegistration):
    username = user.username
    password = user.password

    users_db = read_account_data()

    if username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already taken"
        )

    hashed_password = hash_password(password)

    users_db[username] = {
        "username": username,
        "hashed_password": hashed_password
    }

    with open(json_userfilename, "w") as write_file:
        json.dump(users_db, write_file, indent=4)

    return {"message": "User registered successfully"}






