from fastapi import APIRouter, status

from app.controllers import query_record as query_record_controller
from app.type import queryRecord as query_record_type
from app.type.response import ApiResponse

router = APIRouter()


@router.post("/upload", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def upload(body: query_record_type.CreateQueryRecordBody) -> ApiResponse:
    return query_record_controller.uploadQueryRecord(body)


@router.post("/search", response_model=ApiResponse)
async def search(body: query_record_type.SearchQueryRecordBody) -> ApiResponse:
    return query_record_controller.searchQueryRecord(body)


@router.post("/filter", response_model=ApiResponse)
async def filter_query_records(body: query_record_type.FilterQueryRecordBody) -> ApiResponse:
    return query_record_controller.filterQueryRecord(body)


@router.post("/update", response_model=ApiResponse)
async def update(body: query_record_type.UpdateQueryRecordBody) -> ApiResponse:
    return query_record_controller.updateQueryRecord(body)


@router.post("/remove", response_model=ApiResponse)
async def remove(body: query_record_type.RemoveQueryRecordBody) -> ApiResponse:
    return query_record_controller.removeQueryRecord(body)
