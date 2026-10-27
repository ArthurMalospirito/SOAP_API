from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base


class User(Base):
    __tablename__="users"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(100),nullable=False)
    email: Mapped[str] = mapped_column(nullable=False,unique=True)
    password_hash:Mapped[str] = mapped_column(nullable=False)
    admin:Mapped[bool] = mapped_column(nullable=False,default=False)
    #Isso daqui é para acecssar os eventos do usuário pelo próprio usuário
    events:Mapped[list["Event"]] = relationship(back_populates="user") # type: ignore

    notes:Mapped[list["Note"]] = relationship(back_populates="user") # type: ignore

    def __init__(self,name:str,email:str,password_hash:str,admin:bool=False):
        self.name=name
        self.email=email
        self.password_hash=password_hash
        self.admin=admin
