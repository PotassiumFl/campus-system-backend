from fastapi import APIRouter, status

from app.controllers import campus as campus_controller
from app.type import campus as campus_type

from app.type.response import ApiResponse

router = APIRouter()

@router.post("/upload", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def upload(body: list[campus_type.CreateCampusBody]) -> ApiResponse:
    return campus_controller.uploadCampus(body)