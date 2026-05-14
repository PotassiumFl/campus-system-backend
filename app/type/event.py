from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class EventBody(BaseModel):
    event_id: int | None = Field(default=None)
    building_id: int | None = Field(default=None)
    event_name: str | None = Field(default=None, max_length=128)
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    organizer: str | None = Field(default=None, max_length=128)
    description: str | None = Field(default=None)


class CreateEventBody(EventBody):
    building_id: int = Field(...)
    event_name: str = Field(..., max_length=128)


class UploadEventBody(EventBody):
    building_name: str = Field(..., max_length=64)
    event_name: str = Field(..., max_length=128)
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    organizer: str | None = Field(default=None, max_length=128)
    description: str | None = Field(default=None)

    @field_validator("organizer", "description", mode="before")
    @classmethod
    def empty_str_is_none(cls, v: object) -> object:
        if v == "":
            return None
        return v


class UpdateEventBody(EventBody):
    event_id: int = Field(...)


class RemoveEventBody(EventBody):
    event_id: int = Field(...)


class SearchEventBody(EventBody):
    building_name: str | None = Field(default=None, max_length=64)
    event_name: str | None = Field(default=None, max_length=128)


class FilterEventBody(BaseModel):
    building_name: list[str] = Field(default_factory=list)
    event_name: list[str] = Field(default_factory=list)
    organizer: list[str] = Field(default_factory=list)
    start_time: list[datetime] = Field(default_factory=list)
    end_time: list[datetime] = Field(default_factory=list)
