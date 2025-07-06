from app.schemas.user_schemas import UserAuth
from app.models.user_model import User
from app.core.security import get_password, verify_password
from typing import Optional
from uuid import UUID
from bson import ObjectId


class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        usuario = User(
            email=user.email,
            hash_password=get_password(user.password)
        )

        await usuario.insert()
        usuario_dict = usuario.model_dump()
        usuario_dict["id"] = str(usuario.id)  # ✅ converte o ObjectId para string
        return usuario_dict


    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user
    
    @staticmethod
    async def get_user_by_id(id: UUID) -> Optional[User]:
        user = await User.find_one(User.id == ObjectId(id))
        return user

    @staticmethod
    async def  authenticate_user(email:str, password:str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        if not user: 
            return None
        if not verify_password(
            password=password,
            hashed_password=user.hash_password
            ):
            return None
        return user
    
