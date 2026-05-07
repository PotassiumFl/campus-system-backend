from fastapi import APIRouter, status

from app.controllers import facility as facility_controller
from app.type import facility as facility_type
from app.type.response import ApiResponse

router = APIRouter()


@router.post("/upload", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def upload(body: facility_type.UploadFacilityBody) -> ApiResponse:
    return facility_controller.uploadFacility(body)
