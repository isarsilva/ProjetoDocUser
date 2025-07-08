from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional
class UserAuth(BaseModel):
    username: str = Field(..., min_length=3, max_length=100, description="Nome de Usuário")
    data_nascimento: str = Field(None, description="Data de Nascimento do Usuário")
    cpf: str= Field(None, min_length=11, max_length=11, description="CPF do Usuário")
    celular: str = Field(None, min_length=11, max_length=11, description="Celular do Usuário com DDD")
    email: EmailStr = Field(..., description="E-mail do Usuário")
    password: str = Field(..., min_length=8, max_length=20, description="Senha do Usuário")

class UserDetail(BaseModel):
    id: str
    username: str
    data_nascimento:str = None
    cpf: str = None
    celular: str = None
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None         
    disabled: Optional[bool] = False

class UserAtualiza(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=100)
    data_nascimento: Optional[str] = None  
    cpf: Optional[str] = Field(default=None, min_length=11, max_length=11)
    celular: Optional[str] = Field(default=None, min_length=11, max_length=11)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=20)


   
class UserMe(BaseModel):
    username: str
    email: EmailStr 