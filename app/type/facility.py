from enum import Enum

from pydantic import BaseModel, Field


class FacilityType(Enum):
    dinning = "餐厅"
    waterBar = "水吧"
    studyRoom = "自习室"
    office = "办公室"
    toilet = "卫生间"
    classroom = "教室"
    dormitory = "寝室"
    other = "其他"


class Facility(BaseModel):
    id: int | None = Field(default=None)
    building: str | None = Field(default=None, max_length = 64)
    name: str | None = Field(default=None, max_length = 64)
    type: FacilityType | None = Field(default=None)
    openTime: str | None = Field(default=None, max_length = 128)
