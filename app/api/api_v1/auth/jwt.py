from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Any
from app.services.user_service import UserService
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth_schema import TokenSchema,TokenSchemaWithRefresh, LoginRequest
from app.schemas.user_schemas import UserDetail
from app.models.user_model import User
from app.api.api_v1.dependencies.user_deps import get_current_user
from pydantic import ValidationError
from app.core.config import settings
from app.schemas.auth_schema import TokenPayload
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm




jwt_router = APIRouter()

@jwt_router.post("/login", summary='Cria Access Token e Refresh Token', response_model=TokenSchemaWithRefresh)
async def login(data: OAuth2PasswordRequestForm = Depends()) -> Any:
    usuario = await UserService.authenticate_user(
        email=data.username,  # Aqui o username será seu email
        password=data.password
    )
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou Senha estão incorretos",
        )

    return {
        "access_token": create_access_token(usuario.id),
        "refresh_token": create_refresh_token(usuario.id),
        "token_type": "Bearer"
    }


@jwt_router.post("/refresh-token", summary='Refresh token', response_model=TokenSchema)

async def refresh_token(refresh_token: str = Body(...)):
    print("Executando refresh-token")
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            settings.ALGORITHM
        )
        token_data = TokenPayload(**payload)
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível encontrar o usuário",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": create_access_token(user.user_id),
        "token_type": "Bearer"  
    }