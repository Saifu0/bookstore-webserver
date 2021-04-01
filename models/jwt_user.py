from pydantic import BaseModel

class JWTUser(pydantic):
    username : str
    password : str
    disabled : bool
    role : str
