from pydantic import BaseModel, Field


class Teacher(BaseModel):
    id: int | None = Field(default=None)
    name: str | None = Field(default=None, max_length = 64)
    department: str | None = Field(default=None, max_length = 64)
    email: str | None = Field(default=None, max_length = 128)
