from pydantic import BaseModel
from uuid import UUID

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: UUID = None  
    exp: int = None  

class TokenSchemaWithRefresh(TokenSchema):
        refresh_token: str
