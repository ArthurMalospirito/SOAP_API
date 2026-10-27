from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from security import hash_pw, verify_pw
from models import User

from schemas import UserCreateSchema,UserLoginSchema

auth_router = APIRouter(prefix="/auth",tags=["auth"],dependencies=[])

@auth_router.post("/create_account")
async def create_account(user_create_schema:UserCreateSchema, sesssion:AsyncSession = Depends(get_session)):
    email_result = await sesssion.execute(select(User).filter(User.email==user_create_schema.email))
    email = email_result.scalar_one_or_none()
    if email!=None:
        return {
            "error":True,
            "message":"Esse E-mail já está cadastrado."
            }
    hashed_pw = hash_pw(user_create_schema.password)
    new_user = User(user_create_schema.name,user_create_schema.email,hashed_pw)
    sesssion.add(new_user)
    await sesssion.commit()
    return {
        "error":False,
        "message":"Usuário criado com sucesso."
    }


@auth_router.post("/login")
async def login(user_login_schema:UserLoginSchema,session:AsyncSession = Depends(get_session)):
    user_result = await session.execute(select(User).filter(User.email==user_login_schema.email))
    user = user_result.scalar_one_or_none()
    if user==None:
        return {
            "error": True,
            "message": "Email ou senha incorretos."
        }
    if verify_pw(user_login_schema.password,user.password_hash)==False:
        return {
            "error": True,
            "message": "Email ou senha incorretos."
        }
    #Colocar um JWT aqui no meio para verificação
    return {
        "error": False,
        "message": "Login Efetudado com sucesso."
    }