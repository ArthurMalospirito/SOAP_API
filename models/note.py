from sqlalchemy import String,Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class Note(Base):
    __tablename__="notes"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(String(50),nullable=False)
    text:Mapped[str | None] = mapped_column(Text,nullable=True)
    done:Mapped[bool] = mapped_column(nullable=False,default=False)

    category_id:Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category:Mapped["Category"] = relationship() # type: ignore

    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    user:Mapped["User"] = relationship(back_populates="notes") # type: ignore