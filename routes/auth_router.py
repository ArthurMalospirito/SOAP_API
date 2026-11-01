from fastapi import APIRouter, Depends
from dependencies import get_session, create_jwt, get_refresh_user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from security import hash_pw, verify_pw
from models import User

from schemas import UserCreateSchema,UserLoginSchema
from response_models import SuccessResponse, AppException

auth_router = APIRouter(prefix="/auth",tags=["auth"],dependencies=[])

@auth_router.post("/create_account", response_model=SuccessResponse,status_code=201)
async def create_account(user_create_schema:UserCreateSchema, session:AsyncSession = Depends(get_session)):
    email_result = await session.execute(select(User).where(User.email==user_create_schema.email))
    email = email_result.scalar_one_or_none()
    if email!=None:
        raise AppException(code="EMAIL_ALREADY_EXISTS",status_code=409,message="Esse E-mail já está cadastrado")
    if len(user_create_schema.name)>100:
        raise AppException(code="NAME_ERROR",status_code=400,message="O nome inserido tem mais de 100 caracteres")
    hashed_pw = hash_pw(user_create_schema.password)
    new_user = User(user_create_schema.name,user_create_schema.email,hashed_pw)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    access_token = create_jwt(new_user.id)
    refresh_token = create_jwt(new_user.id,token_type="refresh")
    return SuccessResponse(
        success=True,
        message="Usuário criado com sucesso.",
        data= {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    )


@auth_router.post("/login",response_model=SuccessResponse,status_code=200)
async def login(user_login_schema:UserLoginSchema,session:AsyncSession = Depends(get_session)):
    user_result = await session.execute(select(User).where(User.email==user_login_schema.email))
    user = user_result.scalar_one_or_none()
    if user==None:
        raise AppException(status_code=401,message="Email ou senha incorretos")
    if verify_pw(user_login_schema.password,user.password_hash)==False:
        raise AppException(status_code=401,message="Email ou senha incorretos")
    access_token = create_jwt(user.id)
    refresh_token = create_jwt(user.id,token_type="refresh")
    return SuccessResponse(
        success= True,
        message= "Login Efetudado com sucesso.",
        data= {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    )
    
@auth_router.get("/refresh",response_model=SuccessResponse,status_code=200)
async def use_refresh_token(user:User=Depends(get_refresh_user)):
    access_token = create_jwt(user.id)
    return SuccessResponse(
        success= True,
        message= "Token recarregado com sucesso",
        data= {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    )