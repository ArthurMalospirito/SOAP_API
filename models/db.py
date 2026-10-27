
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase

#Mudar isso para um valor que não pode ser lido diretamente. | .env
engine = create_async_engine("postgresql://postgres:postgres123@localhost:5432/soap",echo=True)

AsyncSession = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)

class Base(DeclarativeBase):
    pass