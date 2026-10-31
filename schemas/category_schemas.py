from pydantic import BaseModel
from typing import Optional
from datetime import date as dateType, time as timeType

class CategorySchema(BaseModel):
    id:int
    name:str
    description:str
    priority:int
    color:str

    class Config:
        from_attributes=True

class CategoryCreateSchema(BaseModel):
    name:str
    description:str
    priority:int
    color:str

    class Config:
        from_attributes=True