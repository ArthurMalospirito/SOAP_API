from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class Event(Base):
    __tablename__="events"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(String(30),nullable=False)
    description:Mapped[str | None] = mapped_column(String(512),nullable=True)
    done:Mapped[bool] = mapped_column(nullable=False,default=False)
    #Acesar usuário pelo evento dele
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    user:Mapped["User"] = relationship(back_populates="events") # type: ignore
    #Acesar categoria do evento
    category_id:Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category:Mapped["Category"] = relationship() # type: ignore