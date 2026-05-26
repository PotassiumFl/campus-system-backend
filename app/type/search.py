from pydantic import BaseModel, Field


class NaturalSearchBody(BaseModel):
    query: str = Field(..., min_length=1)
    user_id: int = Field(...)


class NaturalSearchData(BaseModel):
    answer: str
    raw_results: list[dict]
    query_record: dict
