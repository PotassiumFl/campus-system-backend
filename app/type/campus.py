from pydantic import BaseModel, Field

class CampusBody(BaseModel):
    campus_id: int | None = Field(default=None)
    campus_name: str | None = Field(default=None, max_length=64)
    campus_address: str | None = Field(default=None, max_length=255)

class CreateCampusBody(CampusBody):
    campus_name: str = Field(..., max_length=64)

class UpdateCampusBody(CampusBody):
    campus_id: int = Field(...)


class RemoveCampusBody(CampusBody):
    campus_id: int = Field(...)


class SearchCampusBody(CampusBody):
    pass


class FilterCampusBody(BaseModel):
    campus_name: list[str] = Field(default_factory=list)
    campus_address: list[str] = Field(default_factory=list)
