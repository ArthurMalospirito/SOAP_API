from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

from datetime import date as DateType, time as TimeType

class Event(Base):
    __tablename__="events"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(String(30),nullable=False)
    description:Mapped[str | None] = mapped_column(String(512),nullable=True)
    date:Mapped[DateType] = mapped_column(nullable=False)
    time:Mapped[TimeType | None] = mapped_column(nullable=True)
    done:Mapped[bool] = mapped_column(nullable=False,default=False)
    #Acesar usuário pelo evento dele
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    user:Mapped["User"] = relationship(back_populates="events") # type: ignore
    #Acesar categoria do evento
    category_id:Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category:Mapped["Category"] = relationship() # type: ignore

    def __init__(self,name:str,description:str,user_id:int,category_id:int,date:DateType,done:bool=False,time:TimeType=None):
        self.name=name
        self.description=description
        self.user_id=user_id
        self.category_id=category_id
        self.time=time
        self.date=date
        self.done=done