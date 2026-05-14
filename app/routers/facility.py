from fastapi import APIRouter, status

from app.controllers import facility as facility_controller
from app.type import facility as facility_type
from app.type.response import ApiResponse

router = APIRouter()


@router.post("/upload", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def upload(body: facility_type.UploadFacilityBody) -> ApiResponse:
    return facility_controller.uploadFacility(body)


@router.post("/search", response_model=ApiResponse)
async def search(body: facility_type.SearchFacilityBody) -> ApiResponse:
    return facility_controller.searchFacility(body)


@router.post("/filter", response_model=ApiResponse)
async def filter_facilities(body: facility_type.FilterFacilityBody) -> ApiResponse:
    return facility_controller.filterFacility(body)


@router.post("/update", response_model=ApiResponse)
async def update(body: facility_type.UpdateFacilityBody) -> ApiResponse:
    return facility_controller.updateFacility(body)


@router.post("/remove", response_model=ApiResponse)
async def remove(body: facility_type.RemoveFacilityBody) -> ApiResponse:
    return facility_controller.removeFacility(body)
