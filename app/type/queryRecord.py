from enum import Enum

from pydantic import BaseModel, Field


class QueryType(Enum):
    keyword = "keyword"
    natural_language = "natural_language"


class QueryRecordBody(BaseModel):
    id: int | None = Field(default=None)
    user_id: int | None = Field(default=None)
    query_type: QueryType | None = Field(default=None)
    query_text: str | None = Field(default=None)
    answer: str | None = Field(default=None)


class CreateQueryRecordBody(QueryRecordBody):
    user_id: int = Field(...)
    query_type: QueryType = Field(...)
    query_text: str = Field(...)


class UpdateQueryRecordBody(QueryRecordBody):
    id: int = Field(...)
