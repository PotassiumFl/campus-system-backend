from pydantic import BaseModel, Field
from enum import Enum

class BuildingType(Enum):
    teaching = "教学楼"
    dormitory = "宿舍楼"
    office = "办公楼"
    laboratory = "实验楼"
    gym = "体育馆"
    canteen = "食堂"
    other = "其他"

class Building(BaseModel):
    id: int | None = Field(default=None)
    campus: str | None = Field(default=None, max_length = 64)
    name: str | None = Field(default=None, max_length = 64)
    type: BuildingType | None = Field(default=None)

