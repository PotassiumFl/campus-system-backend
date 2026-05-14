from fastapi import APIRouter, status

from app.controllers import teach as teach_controller
from app.type import teach as teach_type
from app.type.response import ApiResponse

router = APIRouter()


@router.post("/upload", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def upload(body: teach_type.UploadTeachBody) -> ApiResponse:
    return teach_controller.uploadTeach(body)


@router.post("/update", response_model=ApiResponse)
async def update(body: teach_type.UpdateTeachBody) -> ApiResponse:
    return teach_controller.updateTeach(body)


@router.post("/search", response_model=ApiResponse)
async def search(body: teach_type.SearchTeachBody) -> ApiResponse:
    return teach_controller.searchTeach(body)


@router.post("/filter", response_model=ApiResponse)
async def filter_teach(body: teach_type.FilterTeachBody) -> ApiResponse:
    return teach_controller.filterTeach(body)


@router.post("/remove", response_model=ApiResponse)
async def remove(body: teach_type.RemoveTeachBody) -> ApiResponse:
    return teach_controller.removeTeach(body)
