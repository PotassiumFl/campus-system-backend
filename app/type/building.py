from enum import Enum

from pydantic import BaseModel, Field, field_validator

class BuildingType(Enum):
    teaching = "教学楼"
    dormitory = "宿舍楼"
    office = "办公楼"
    laboratory = "实验楼"
    gym = "体育馆"
    canteen = "食堂"
    other = "其他"

class BuildingBody(BaseModel):
    id: int | None = Field(default=None)
    campus_id: int | None = Field(default=None)
    name: str | None = Field(default=None, max_length = 64)
    type: BuildingType | None = Field(default=None)


class CreateBuildingBody(BuildingBody):
    name: str = Field(...,max_length=64)
    campus_id: int = Field(...)
    type: BuildingType = Field(BuildingType.other)


class UploadBuildingBody(BaseModel):
    building_name: str = Field(..., max_length=64)
    campus_name: str = Field(..., max_length=64)
    building_type: BuildingType = Field(default=BuildingType.other)

    @field_validator("building_type", mode="before")
    @classmethod
    def null_building_type_is_other(cls, v: object) -> object:
        return BuildingType.other if v is None else v


class UpdateBuildingBody(BuildingBody):
    id: int = Field(...)