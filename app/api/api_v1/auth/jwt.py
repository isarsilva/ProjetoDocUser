from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Any
from app.services.user_service import UserService
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth_schema import TokenSchema, TokenSchemaWithRefresh, TokenPayload
from app.models.user_model import User
from app.api.api_v1.dependencies.user_deps import get_current_user
from pydantic import ValidationError
from app.core.config import settings
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm

jwt_router = APIRouter()

# Endpoint de login
@jwt_router.post("/login", summary="Cria Access Token e Refresh Token", response_model=TokenSchemaWithRefresh)
async def login(data: OAuth2PasswordRequestForm = Depends()) -> Any:
    usuario = await UserService.authenticate_user(
        email=data.username,
        password=data.password
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha estão incorretos",
        )

    return {
        "access_token": create_access_token(usuario.id),
        "refresh_token": create_refresh_token(usuario.id),
        "token_type": "Bearer"
    }

# Endpoint de refresh
@jwt_router.post("/refresh-token", summary="Refresh token", response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            settings.ALGORITHM
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = await UserService.get_user_by_id(token_data.sub)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível encontrar o usuário",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": create_access_token(usuario.id),
        "token_type": "Bearer"
    }
