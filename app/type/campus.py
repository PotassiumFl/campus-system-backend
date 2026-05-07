from pydantic import BaseModel, Field

class CampusBody(BaseModel):
    id: int | None = Field(default=None)
    name: str | None = Field(default=None, max_length=64)
    address: str | None = Field(default=None, max_length=255)

class CreateCampusBody(CampusBody):
    name: str = Field(..., max_length=64)

class UpdateCampusBody(CampusBody):
    id: int = Field(...)
