
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase

from main import DATABASE_URL
#Mudar isso para um valor que não pode ser lido diretamente. | .env
engine = create_async_engine(DATABASE_URL,echo=True)

AsyncSession = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)

class Base(DeclarativeBase):
    pass