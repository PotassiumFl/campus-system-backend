from enum import Enum

from pydantic import BaseModel, Field, field_validator


class FacilityType(Enum):
    restaurant = "餐厅"
    waterBar = "水吧"
    studyRoom = "自习室"
    office = "办公室"
    toilet = "卫生间"
    classroom = "教室"
    dormitory = "寝室"
    other = "其他"


class FacilityBody(BaseModel):
    id: int | None = Field(default=None)
    building_id: int | None = Field(default=None)
    name: str | None = Field(default=None, max_length = 64)
    type: FacilityType | None = Field(default=None)
    openTime: str | None = Field(default=None, max_length = 128)


class CreateFacilityBody(FacilityBody):
    building_id: int = Field(...)
    name: str = Field(...)
    type: FacilityType = Field(...)


class UploadFacilityBody(BaseModel):
    building_name: str = Field(..., max_length=64)
    facility_name: str = Field(..., max_length=64)
    facility_type: FacilityType = Field(default=FacilityType.other)
    openTime: str | None = Field(default=None, max_length=128)

    @field_validator("openTime", mode="before")
    @classmethod
    def empty_open_time_is_none(cls, v: object) -> object:
        if v is None or v == "":
            return None
        return v


class UpdateFacilityBody(FacilityBody):
    id: int = Field(...)