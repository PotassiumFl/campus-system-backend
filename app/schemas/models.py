from typing import Any, Optional

from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    success: bool
    code: int
    message: str | None
    data: Any | None = None


class RegisterBody(BaseModel):
    name: str = Field(..., min_length = 1, max_length = 128)
    password: str = Field(..., min_length = 1)


class LoginBody(RegisterBody):
    """Currently same shape as RegisterBody."""


class searchCourseBody(BaseModel):
    course_id: list[str] = Field(..., min_length = 0, max_length = 128)
    course_name: list[str] = Field(..., min_length = 0, max_length = 128)
    credit: list[int] = Field(..., min_length = 0, max_length = 128)
    department: list[str] = Field(..., min_length = 0, max_length = 128)
    semester: list[str] = Field(..., min_length = 0, max_length = 128)


class CourseBody(BaseModel):
    course_id: str
    course_name: str
    credit: float
    department: str
    semester: str


class uploadCourseBody(CourseBody):
    """Currently same shape as CourseBody."""