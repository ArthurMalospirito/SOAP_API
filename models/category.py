from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class Category(Base):
    __tablename__="categories"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(String(30),nullable=False)
    description:Mapped[str | None] = mapped_column(String(512),nullable=True)
    priority:Mapped[int]= mapped_column(nullable=False,default=0)
    color: Mapped[str] = mapped_column(String(16),nullable=False,default="#FFFFFF")

