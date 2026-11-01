from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dependencies import get_session
from response_models import AppException

from models import User

from jose import jwt, JWTError # type: ignore
from datetime import datetime, timedelta,timezone
from main import ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_DAYS,ALGORITHM, SECRET_KEY, http_bearer_refresh,http_bearer_access

def create_jwt(user_id:int,token_type:str="access"):
    if token_type=="access":
        exp=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    elif token_type=="refresh":
        exp=datetime.now(timezone.utc)+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    else:
        raise AppException(code="WRONG_TOKEN_TYPE",status_code=400,message="Erro ao escolher tipo de token")
    payload = {
        "sub": str(user_id),
        "exp": exp,
        "type":token_type
    }
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

async def verify_jwt(token:str,session:AsyncSession, expected_type:str="access") -> User:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        token_type=payload.get("type")
        if token_type!=expected_type:
            raise AppException(code="INVALID_TOKEN_TYPE",status_code=401,message=f"Token inválido. Esperado {expected_type}, recebido {token_type}")
    except JWTError as error:   
        raise AppException(code="ACCESS_DENIED",status_code=401,message="Acesso negado, verifique a validade do Token")

    user_result = await session.execute(select(User).where(User.id==user_id))
    user= user_result.scalar_one_or_none()
    if user==None:
        raise AppException(code="USER_NOT_FOUND",status_code=401,message="Usuário não encontrado")
    
    return user

async def get_current_user(
    credentials:HTTPAuthorizationCredentials=Depends(http_bearer_access),
    session: AsyncSession = Depends(get_session)
) -> User:
    return await verify_jwt(credentials.credentials, session, expected_type="access")


async def get_refresh_user(
    credentials:HTTPAuthorizationCredentials=Depends(http_bearer_refresh),
    session: AsyncSession = Depends(get_session)
) -> User:
    return await verify_jwt(credentials.credentials, session, expected_type="refresh")