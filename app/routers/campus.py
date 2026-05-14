from fastapi import APIRouter, status

from app.controllers import campus as campus_controller
from app.type import campus as campus_type

from app.type.response import ApiResponse

router = APIRouter()

@router.post("/upload", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def upload(body: campus_type.CreateCampusBody) -> ApiResponse:
    return campus_controller.uploadCampus(body)


@router.post("/search", response_model=ApiResponse)
async def search(body: campus_type.SearchCampusBody) -> ApiResponse:
    return campus_controller.searchCampus(body)


@router.post("/filter", response_model=ApiResponse)
async def filter_campus(body: campus_type.FilterCampusBody) -> ApiResponse:
    return campus_controller.filterCampus(body)


@router.post("/update", response_model=ApiResponse)
async def update(body: campus_type.UpdateCampusBody) -> ApiResponse:
    return campus_controller.updateCampus(body)


@router.post("/remove", response_model=ApiResponse)
async def remove(body: campus_type.RemoveCampusBody) -> ApiResponse:
    return campus_controller.removeCampus(body)