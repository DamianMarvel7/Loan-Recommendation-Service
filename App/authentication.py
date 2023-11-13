# from fastapi import FastAPI, Depends, HTTPException, status, Request, Form,APIRouter
# from fastapi.responses import RedirectResponse
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from fastapi.middleware.cors import CORSMiddleware
# import os
# import pathlib
# import requests
# from google.oauth2 import id_token
# from google_auth_oauthlib.flow import Flow
# from pip._vendor import cachecontrol
# from google.auth.transport.requests import Request as GoogleRequest
# import os

# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# app = APIRouter()
# # config = Config(".env")
# # app.add_middleware(SessionMiddleware, secret_key=config("SECRET_KEY", default="TSTGANTENGBANGETTT"))

# GOOGLE_CLIENT_ID = "408921090634-q3k9gmkpl201vc6e4g3omf93qkqste94.apps.googleusercontent.com"
# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

# flow = Flow.from_client_secrets_file(
#     client_secrets_file=client_secrets_file,
#     scopes=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
#     redirect_uri="http://loanrecommendation.a9hwc6bcfeebc6gu.eastus.azurecontainer.io:8080/callback"
# )

# @app.get("/")
# async def index():
#     return "Login dulu ya kak"

# @app.get("/login")
# async def login(request: Request):
#     authorization_url, state = flow.authorization_url()
#     request.session["state"] = state
    
#     return RedirectResponse(authorization_url)


# @app.get("/callback")
# async def callback(request: Request):
#     session_state = request.session["state"]
#     # print(session_state)
#     # print(request.query_params.get("state"))
#     # if session_state != request.query_params.get("state"):
#     #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="State mismatch")

#     flow.fetch_token(authorization_response=str(request.url))

#     credentials = flow.credentials

#     id_info = id_token.verify_oauth2_token(
#         id_token=credentials.id_token,
#         request=GoogleRequest(),
#         audience=GOOGLE_CLIENT_ID
#     )

#     request.session["google_id"] = id_info.get("sub")
#     request.session["name"] = id_info.get("name")
    
#     print(request.session)
#     return RedirectResponse("/customers")


# @app.get("/logout")
# async def logout(request: Request):
#     request.session.clear()
#     return RedirectResponse("/")


# @app.get("/protected_area")
# async def protected_area(request: Request):
#     if "google_id" not in request.session:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     return {"google_id": request.session["google_id"], "name": request.session["name"]}


from fastapi import FastAPI, Depends, status, Header, Request, HTTPException,APIRouter
import json
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import uuid
import bcrypt
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from Utility.utils import  encode_token, decode_token

class Customer(BaseModel):
    Customer_ID: str
    Gender: str
    Married: str
    Dependents: str
    Education: str
    ApplicantIncome: int
    Property_Area: str
    Username: str
    


app = APIRouter()


json_userfilename = "user.json"



def read_account_data():
    
    with open(json_userfilename, "r") as read_file:
        data = json.load(read_file)
    return data





def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str
    
class UserRegistration(BaseModel):
    username: str
    password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# Example of how to decode a token and get the user
def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_token(token)
    fake_users_db = read_account_data()
    
    user = get_user(fake_users_db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user



async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@app.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    fake_users_db = read_account_data()

    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)

    # Verify the password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Generate token (this part needs to be implemented)
    token = encode_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/register")
async def register_user(user: UserRegistration):
    username = user.username
    password = user.password

    # Load the existing users
    fake_users_db = read_account_data()

    # Check if the user already exists
    if username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already taken"
        )

    # Hash the password
    hashed_password = hash_password(password)

    # Add the user to the database
    fake_users_db[username] = {
        "username": username,
        "hashed_password": hashed_password
    }

    # Save the updated users back to the file
    with open(json_userfilename, "w") as write_file:
        json.dump(fake_users_db, write_file, indent=4)

    return {"message": "User registered successfully"}





