from fastapi import APIRouter, status

from app.controllers import building as building_controller
from app.type import building as building_type
from app.type.response import ApiResponse

router = APIRouter()


@router.post("/upload", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def upload(body: building_type.UploadBuildingBody) -> ApiResponse:
    return building_controller.uploadBuilding(body)