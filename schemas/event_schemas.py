from pydantic import BaseModel
from typing import Optional
from datetime import date as dateType, time as timeType

class EventSchema(BaseModel):
    id:int
    name:str
    description:str |None = None
    date: dateType
    time: timeType | None = None
    done:Optional[bool]=None
    user_id:int
    category_id:int

    class Config:
        from_attributes=True

class EventCreateSchema(BaseModel):
    name:str
    description:str
    date: dateType
    time: timeType | None = None
    done:Optional[bool]=False
    category_id:int

    class Config:
        from_attributes=True