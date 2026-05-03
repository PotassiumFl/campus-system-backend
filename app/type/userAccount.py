from pydantic import BaseModel, Field
from enum import Enum


class UserRole(Enum):
    user = "user"
    admin = "admin"


class UserAccount(BaseModel):
    id: int | None = Field(default=None)
    name: str | None = Field(default=None, max_length = 32)
    password: str | None = Field(default=None, max_length = 128)
    role: UserRole | None = Field(default=None)
