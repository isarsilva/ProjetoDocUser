from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional
class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="E-mail do Usuário")
    username: str = Field(..., min_length=4, max_length=50, description="Username do Usuário")
    password: str = Field(..., min_length=8, max_length=20, description="Senha do Usuário")

class UserDetail(BaseModel):
    id: str
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None         
    disabled: Optional[bool] = False