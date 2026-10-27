from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name:str
    email:str
    password_hash:str
    admin:Optional[bool]=False

    class Config:
        from_attributes=True

class UserCreateSchema(BaseModel):
    name:str
    email:str
    password:str

    class Config:
        from_attributes=True

class UserLoginSchema(BaseModel):
    email:str
    password:str

    class Config:
        from_attributes=True