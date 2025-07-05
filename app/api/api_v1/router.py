from fastapi import APIRouter
from handlers.user import user_router


router = APIRouter(prefix="/users")

router.include_router(
    user_router,
    prefix="/users",
    tags=["users"]
)