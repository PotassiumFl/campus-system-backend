from pydantic import BaseModel, Field


class CourseBody(BaseModel):
    id: int | None = Field(default = None)
    name: str | None = Field(default = None, max_length = 128)
    credit: float | None = Field(default = None, ge = 0, le = 10)
    department: str | None = Field(default = None, max_length = 64)
    semester: str | None = Field(default = None, max_length = 16)
    section_no: str | None = Field(default = None, max_length = 16)


class CreateCourseBody(CourseBody):
    name: str = Field(..., max_length = 128)
    semester: str = Field(..., max_length = 16)
    section_no: str = Field(..., max_length = 16)


class UpdateCourseBody(CourseBody):
    id: int = Field(...)
