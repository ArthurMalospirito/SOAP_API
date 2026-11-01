from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from response_models import AppException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(
    title="S.O.A.P. API",
    description="API de gerenciamento do S.O.A.P",
    version="Beta 1.0.0"
)

ALLOWED_ORIGINS = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"]

)


@app.exception_handler(AppException)
async def app_exception_handler(request, exc:AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success":False,
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