from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user_schemas import UserAuth, UserDetail
from app.services.user_service import UserService
import pymongo
from beanie.exceptions import RevisionIdWasChanged 
from app.models.user_model import User
from app.api.api_v1.dependencies.user_deps import get_current_user



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

@user_router.get("/me", summary="Detalhes do Usuario Logado", response_model=UserDetail)
async def get_me(user: User = Depends(get_current_user)):
    return UserDetail.model_validate(user.model_dump())

   