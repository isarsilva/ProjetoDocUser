from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schemas import UserAuth
from app.services.user_service import UserService
import pymongo

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/adiciona", summary="Adiciona um usuário")
async def adiciona_usuario(data: UserAuth):
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já existe"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
