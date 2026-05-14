from enum import Enum

from pydantic import BaseModel, Field


class UserRole(Enum):
    user = "user"
    admin = "admin"


class UserAccountBody(BaseModel):
    user_id: int | None = Field(default=None)
    username: str | None = Field(default=None, max_length=32)
    password: str | None = Field(default=None, max_length=255)
    user_role: UserRole | None = Field(default=None)


class CreateUserAccountBody(UserAccountBody):
    username: str = Field(..., max_length=32)
    password: str = Field(..., max_length=255)
    user_role: UserRole = Field(default=UserRole.user)


class AuthRegisterBody(UserAccountBody):
    username: str = Field(..., max_length=32)
    password: str = Field(..., max_length=255)


class AuthLoginBody(UserAccountBody):
    username: str = Field(..., max_length=32)
    password: str = Field(..., max_length=255)


class AuthUpdateBody(UserAccountBody):
    user_id: int = Field(...)
    password: str | None = Field(default=None, max_length=255)


class UpdateUserAccountBody(UserAccountBody):
    user_id: int = Field(...)
