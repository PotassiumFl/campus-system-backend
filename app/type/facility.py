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
    facility_id: int | None = Field(default=None)
    building_id: int | None = Field(default=None)
    facility_name: str | None = Field(default=None, max_length = 64)
    facility_type: FacilityType | None = Field(default=None)
    openTime: str | None = Field(default=None, max_length = 128)


class CreateFacilityBody(FacilityBody):
    building_id: int = Field(...)
    facility_name: str = Field(...)
    facility_type: FacilityType = Field(...)


class UploadFacilityBody(FacilityBody):
    building_name: str = Field(..., max_length=64)
    facility_name: str = Field(..., max_length=64)
    facility_type: FacilityType = Field(default=FacilityType.other)

    @field_validator("openTime", mode="before")
    @classmethod
    def empty_open_time_is_none(cls, v: object) -> object:
        if v is None or v == "":
            return None
        return v


class UpdateFacilityBody(FacilityBody):
    facility_id: int = Field(...)


class RemoveFacilityBody(FacilityBody):
    facility_id: int = Field(...)


class SearchFacilityBody(FacilityBody):
    building_name: str | None = Field(default=None, max_length=64)
    facility_name: str | None = Field(default=None, max_length=64)


class FilterFacilityBody(BaseModel):
    building_name: list[str] = Field(default_factory=list)
    facility_name: list[str] = Field(default_factory=list)
    facility_type: list[FacilityType] = Field(default_factory=list)
    open_time: list[str] = Field(default_factory=list)
