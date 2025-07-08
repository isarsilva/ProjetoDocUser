from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user_schemas import UserAuth, UserDetail
from app.services.user_service import UserService
import pymongo
from beanie.exceptions import RevisionIdWasChanged 
from app.models.user_model import User
from app.api.api_v1.dependencies.user_deps import get_current_user



user_router = APIRouter(tags=["Users"])


@user_router.post("/register", summary="Adiciona um usuário", response_model=UserDetail)
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

@user_router.put("update/{user_id}", summary="Atualiza um usuário", response_model=UserDetail)
async def atualiza_usuario(user_id:str, data: UserAuth, user: User = Depends(get_current_user)):    
    try:
        user_to_update = await UserService.get_user_by_id(user_id)
        if not user_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        user_to_update.username = data.username
        user_to_update.data_nascimento = data.data_nascimento
        user_to_update.cpf = data.cpf
        user_to_update.celular = data.celular
        user_to_update.email = data.email
        user_to_update.hash_password = UserService.get_password(data.password)

        await user_to_update.save()
        
        return UserDetail.model_validate(user_to_update.model_dump())
    except RevisionIdWasChanged:
        raise HTTPException(
            status_code=409,
            detail="Conflito: o documento foi alterado por outro processo. Atualize e tente novamente."
        )
@user_router.delete("/delete/{user_id}", summary="Deleta um usuário")
async def apaga_usuario(user_id: str, user: User = Depends(get_current_user)):
    try:
        user_to_delete = await UserService.get_user_by_id(user_id)
        
        if not user_to_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )

        await user_to_delete.delete()
        return {"message": "Usuário deletado com sucesso"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar usuário: {str(e)}"
        )

@user_router.get("/me", summary="Detalhes do Usuario Logado", response_model=UserDetail)
async def get_me(user: User = Depends(get_current_user)):
    return UserDetail.model_validate(user.model_dump())

   