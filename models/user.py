from pydantic import BaseModel
import enum
from fastapi import Query

class Role(enum.Enum):
    admin = "admin"
    personal = "personal"

class User(BaseModel):
    name : str
    password : str
    mail : str = Query(..., regex='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
    role : Role

# those 3 dots mean it is required, we can replace those 
# 3 dots with None or some default values