from pydantic import BaseModel, Field, field_validator


class CourseBody(BaseModel):
    course_id: str | None = Field(default=None, max_length=16)
    course_name: str | None = Field(default=None, max_length=128)
    credit: float | None = Field(default=None, ge=0, le=10)
    department: str | None = Field(default=None, max_length=64)


class CreateCourseBody(CourseBody):
    course_id: str = Field(..., max_length=16)
    course_name: str = Field(..., max_length=128)


class UploadCourseBody(CourseBody):
    course_id: str = Field(..., max_length=16)
    course_name: str = Field(..., max_length=128)
    credit: float | None = Field(default=None, ge=0, le=10)
    department: str | None = Field(default=None, max_length=64)

    @field_validator("department", mode="before")
    @classmethod
    def empty_department_is_none(cls, v: object) -> object:
        if v == "":
            return None
        return v


class UpdateCourseBody(CourseBody):
    course_id: str = Field(..., max_length=16)


class RemoveCourseBody(CourseBody):
    course_id: str = Field(..., max_length=16)


class SearchCourseBody(CourseBody):
    pass


class FilterCourseBody(BaseModel):
    course_id: list[str] = Field(default_factory=list)
    course_name: list[str] = Field(default_factory=list)
    department: list[str] = Field(default_factory=list)
    credit: list[float] = Field(default_factory=list)
