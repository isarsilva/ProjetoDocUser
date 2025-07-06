from fastapi import APIRouter
from app.api.api_v1.handlers.user import user_router
from app.api.api_v1.auth.jwt import jwt_router

router = APIRouter()

router.include_router(
    user_router,
    prefix="/user",
    tags=["Users"]
)

router.include_router(
    jwt_router,
    prefix="/auth",  
    tags=["Auth"]
)
