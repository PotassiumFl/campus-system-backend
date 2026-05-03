from pydantic import BaseModel, Field
from datetime import time

class Event(BaseModel):
    id: int | None = Field(default=None)
    building: str | None = Field(default=None)
    name: str | None = Field(default=None, max_length = 128)
    start_time: time | None = Field(default=None)
    end_time: time | None = Field(default=None)
    organizer: str | None = Field(default=None, max_length = 128)
    description: str | None = Field(default=None)
