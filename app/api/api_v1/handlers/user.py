from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schemas import UserAuth, UserDetail
from app.services.user_service import UserService
import pymongo
from beanie.exceptions import RevisionIdWasChanged 


user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/adiciona", summary="Adiciona um usuário", response_model=UserDetail)
async def adiciona_usuario(data: UserAuth):
    try:
        return await UserService.create_user(data)
    
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário com este nome ou e-mail já existe"
        )

    except RevisionIdWasChanged:
        raise HTTPException(
            status_code=409,
            detail="Conflito: o documento foi alterado por outro processo. Atualize e tente novamente."
        )

   