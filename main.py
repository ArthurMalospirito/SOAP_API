from fastapi import FastAPI

from response_models import AppException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer,HTTPBearer

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

app = FastAPI()


@app.exception_handler(AppException)
async def app_exception_handler(request, exc:AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "sucess":False,
            "error": {
                "code":exc.code,
                "message": exc.message
            }
        }
    )

http_bearer_access = HTTPBearer(description="Access Token")
http_bearer_refresh = HTTPBearer(description="Refresh Token")

from routes import auth_router, event_router,category_router

app.include_router(auth_router)
app.include_router(event_router)
app.include_router(category_router)