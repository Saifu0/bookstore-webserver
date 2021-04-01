from datetime import datetime, timedelta
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from models.jwt_user import JWTUser
from passlib.context import CryptContext
from utils.const import (JWT_ALGORITHM, JWT_EXPIRATION_TIME_MINUTES,
                         JWT_SECRET_KEY)
from starlette.status import HTTP_401_UNAUTHORIZED

pwd_context = CryptContext(schemes="bcrypt")
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")

jwt_user1 = {
    "usernmae" : "user1",
    "password" : "$2b$12$zxIItOsEyTO13Ttb/aCiSOUdtkF7Ht9.RbDo4TWUJ0EXR2oYJiZR6",
    "disabled" : False,
    "role" : "admin"
}
jwt_user1_obj = JWTUser(**jwt_user1)

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password,hashed_password)
    except Exception as e:
        return False

print(get_hashed_password("pass1"))

def authenticate_user(username : str, password : str):
    if jwt_user1_obj.username == username:
        if verify_password(password, jwt_user1_obj.password) == True:
            return True
    return False

def create_jwt_token(username : str):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {
        "sub" : username,
        "exp" : expiration
    }
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm = JWT_ALGORITHM)
    return { "token" : jwt_token }

def check_jwt_token(token : str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        expiration = jwt_payload.get("exp")
        if datetime.utcnow() < expiration:
            if jwt_user1_obj.username == username:
                return final_checks(username)
    except Exception as e:
        return HTTP_401_UNAUTHORIZED
    return HTTP_401_UNAUTHORIZED

def final_checks(username : str):
    pass