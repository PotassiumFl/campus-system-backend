from enum import Enum

from pydantic import BaseModel, Field, field_validator

class BuildingType(Enum):
    teaching = "教学楼"
    dormitory = "宿舍楼"
    office = "办公楼"
    laboratory = "实验楼"
    gym = "体育馆"
    canteen = "食堂"
    library = "图书馆"
    other = "其他"

class BuildingBody(BaseModel):
    building_id: int | None = Field(default=None)
    campus_id: int | None = Field(default=None)
    building_name: str | None = Field(default=None, max_length = 64)
    building_type: BuildingType | None = Field(default=None)


class CreateBuildingBody(BuildingBody):
    building_name: str = Field(...,max_length=64)
    campus_id: int = Field(...)
    building_type: BuildingType = Field(BuildingType.other)


class UploadBuildingBody(BuildingBody):
    building_name: str = Field(..., max_length=64)
    campus_name: str = Field(..., max_length=64)
    building_type: BuildingType = Field(default=BuildingType.other)

    @field_validator("building_type", mode="before")
    @classmethod
    def null_building_type_is_other(cls, v: object) -> object:
        return BuildingType.other if v is None else v


class UpdateBuildingBody(BuildingBody):
    building_id: int = Field(...)


class RemoveBuildingBody(BuildingBody):
    building_id: int = Field(...)


class SearchBuildingBody(BuildingBody):
    campus_name: str | None = Field(default=None, max_length=64)
    building_name: str | None = Field(default=None, max_length=64)


class FilterBuildingBody(BaseModel):
    campus_name: list[str] = Field(default_factory=list)
    building_name: list[str] = Field(default_factory=list)
    building_type: list[BuildingType] = Field(default_factory=list)
