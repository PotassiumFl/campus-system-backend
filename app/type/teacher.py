from pydantic import BaseModel, Field, field_validator


class TeacherBody(BaseModel):
    teacher_id: int | None = Field(default=None)
    teacher_name: str | None = Field(default=None, max_length=64)
    department: str | None = Field(default=None, max_length=64)
    email: str | None = Field(default=None, max_length=64)

    @field_validator("email", mode="before")
    @classmethod
    def empty_email_is_none(cls, v: object) -> object:
        if v == "":
            return None
        return v


class CreateTeacherBody(TeacherBody):
    teacher_name: str = Field(..., max_length=64)


class UploadTeacherBody(TeacherBody):
    teacher_name: str = Field(..., max_length=64)
    department: str | None = Field(default=None, max_length=64)
    email: str | None = Field(default=None, max_length=64)

    @field_validator("email", "department", mode="before")
    @classmethod
    def empty_str_is_none(cls, v: object) -> object:
        if v == "":
            return None
        return v


class UpdateTeacherBody(TeacherBody):
    teacher_id: int = Field(...)


class RemoveTeacherBody(TeacherBody):
    teacher_id: int = Field(...)


class SearchTeacherBody(TeacherBody):
    pass


class FilterTeacherBody(BaseModel):
    teacher_name: list[str] = Field(default_factory=list)
    department: list[str] = Field(default_factory=list)
    email: list[str] = Field(default_factory=list)
