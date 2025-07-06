from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from fastapi import Depends,HTTPException, status
from app.models.user_model import User
from jose import jwt 
from app.schemas.auth_schema import TokenPayload 
from datetime import datetime
from pydantic import ValidationError
from app.services.user_service import UserService
from uuid import UUID

oauth_reusavel = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    scheme_name="JWT",
)

async def get_current_user(token: str = Depends(oauth_reusavel)) -> User:
    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Token data
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token foi expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Erro na validação do token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Aqui você pode buscar o usuário
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário não encontrado"
        )
    return user