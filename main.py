from fastapi import FastAPI
from core import config
from database import models
from products import router as product_router
from users import router as user_router
from auth import router as auth_router

app = FastAPI(title = "Mi app", version = "0.0.1")

app.include_router(product_router.api_router)
app.include_router(user_router.api_router)
app.include_router(auth_router.api_router)
