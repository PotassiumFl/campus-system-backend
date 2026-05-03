from datetime import time

from pydantic import BaseModel, Field
from enum import Enum

class QueryType(Enum):
    keyword = "keyword"
    naturalLanguage = "naturalLanguage"

class QueryRecord(BaseModel):
    id: int | None = Field(default=None)
    userId: int | None = Field(default=None)
    type: QueryType | None = Field(default=None)
    queryTime: time | None = Field(default=None)
    queryText: str | None = Field(default=None)
    answer: str | None = Field(default=None)
