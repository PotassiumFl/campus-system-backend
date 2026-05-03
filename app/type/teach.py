from datetime import time

from pydantic import BaseModel, Field
from enum import Enum

class TeachRole(Enum):
    teacher = "教师"
    assistant = "助教"

class Teach(BaseModel):
    teacherId: int | None = Field(default=None)
    courseId: int | None = Field(default=None)
    role: TeachRole | None = Field(default=None)
    startTime: time | None = Field(default=None)
    endTime: time | None = Field(default=None)
