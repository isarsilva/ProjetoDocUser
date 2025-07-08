from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from app.models.user_model import User
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from app.schemas.auth_schema import TokenPayload
from datetime import datetime, timezone
from pydantic import ValidationError
from app.services.user_service import UserService

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
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTClaimsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro nas claims do token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user
