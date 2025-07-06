from pydantic import BaseModel, Field, EmailStr, field_serializer
from beanie import Document, Indexed
from bson import ObjectId
from typing import Optional
from datetime import datetime

class User(Document):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    email: EmailStr = Indexed(unique=True)
    hash_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = False

    model_config = {"arbitrary_types_allowed": True}

    @field_serializer("id")
    def serialize_id(self, id_value):
        return str(id_value)

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False

    @property
    def create(self) -> datetime:
        return self.id.generation_time

    @classmethod
    async def by_email(cls, email: str) -> "User":
        return await cls.find_one(cls.email == email)
