from passlib.context import CryptContext
from typing import Union, Any
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings  # Importando as configurações do projeto

password_context = CryptContext( # para criar o contexto de criptografia
    schemes=["bcrypt"], 
    deprecated="auto"
    )

def get_password(password: str) -> str: # para criptografar a senha
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool: # para verificar se a senha é igual a senha criptografada
    return password_context.verify(password, hashed_password)

def create_access_token(subject: str, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    expire = datetime.utcnow() + expires_delta
    info_jwt = {
        "sub": str(subject),
        "exp": int(expire.timestamp())  # <-- Corrigido aqui!
    }
    jwt_encoded = jwt.encode(
        info_jwt,
        settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return jwt_encoded
def create_refresh_token(subject: Union[str, Any], expires_delta:int =None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta 
    else:
        expires_delta= datetime.utcnow() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRATION_MINUTES
    )
    info_jwt = {
      "exp":  expires_delta,
      "sub": str(subject)
    }
    jwt_encoded = jwt.encode(
        info_jwt,
        settings.JWT_REFRESH_SECRET_KEY,
        settings.ALGORITHM
    )
    return jwt_encoded