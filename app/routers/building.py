from fastapi import APIRouter, status

from app.controllers import building as building_controller
from app.type import building as building_type
from app.type.response import ApiResponse

router = APIRouter()


@router.post("/upload", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def upload(body: building_type.UploadBuildingBody) -> ApiResponse:
    return building_controller.uploadBuilding(body)


@router.post("/search", response_model=ApiResponse)
async def search(body: building_type.SearchBuildingBody) -> ApiResponse:
    return building_controller.searchBuilding(body)


@router.post("/filter", response_model=ApiResponse)
async def filter_buildings(body: building_type.FilterBuildingBody) -> ApiResponse:
    return building_controller.filterBuilding(body)


@router.post("/update", response_model=ApiResponse)
async def update(body: building_type.UpdateBuildingBody) -> ApiResponse:
    return building_controller.updateBuilding(body)


@router.post("/remove", response_model=ApiResponse)
async def remove(body: building_type.RemoveBuildingBody) -> ApiResponse:
    return building_controller.removeBuilding(body)