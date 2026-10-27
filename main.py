from fastapi import FastAPI

#Ainda nãao usado, mas importante
from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

from routes import auth_router

app.include_router(auth_router)