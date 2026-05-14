from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TeachRole(Enum):
    teacher = "教师"
    assistant = "助教"


class TeachBody(BaseModel):
    teacher_id: int | None = Field(default=None)
    course_id: str | None = Field(default=None, max_length=16)
    semester: str | None = Field(default=None, max_length=16)
    section_no: str | None = Field(default=None, max_length=16)
    role: TeachRole | None = Field(default=None)
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)


class CreateTeachBody(TeachBody):
    teacher_id: int = Field(...)
    course_id: str = Field(..., max_length=16)
    semester: str = Field(..., max_length=16)
    section_no: str = Field(..., max_length=16)
    role: TeachRole = Field(default=TeachRole.teacher)


class UploadTeachBody(TeachBody):
    teacher_id: int = Field(...)
    course_id: str = Field(..., max_length=16)
    semester: str = Field(..., max_length=16)
    section_no: str = Field(..., max_length=16)


class UpdateTeachBody(TeachBody):
    teacher_id: int = Field(...)
    course_id: str = Field(..., max_length=16)
    semester: str = Field(..., max_length=16)
    section_no: str = Field(..., max_length=16)


class RemoveTeachBody(TeachBody):
    teacher_id: int = Field(...)
    course_id: str = Field(..., max_length=16)
    semester: str = Field(..., max_length=16)
    section_no: str = Field(..., max_length=16)


class SearchTeachBody(TeachBody):
    pass


class FilterTeachBody(BaseModel):
    teacher_id: list[int] = Field(default_factory=list)
    course_id: list[str] = Field(default_factory=list)
    semester: list[str] = Field(default_factory=list)
    section_no: list[str] = Field(default_factory=list)
    role: list[TeachRole] = Field(default_factory=list)
