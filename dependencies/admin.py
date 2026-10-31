from fastapi import Depends
from dependencies import get_current_user
from response_models import AppException
from models import User

async def verify_admin(user:User=Depends(get_current_user)):
    if not user.admin:
        raise AppException(code="ACCESS_FORBIDDEN",status_code=403,message="Você não tem acesso de administrador para esta rota.")
    return user