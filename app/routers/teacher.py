from fastapi import APIRouter, status

from app.controllers import teacher as teacher_controller
from app.type import teacher as teacher_type
from app.type.response import ApiResponse

router = APIRouter()


@router.post("/upload", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def upload(body: teacher_type.UploadTeacherBody) -> ApiResponse:
    return teacher_controller.uploadTeacher(body)


@router.post("/search", response_model=ApiResponse)
async def search(body: teacher_type.SearchTeacherBody) -> ApiResponse:
    return teacher_controller.searchTeacher(body)


@router.post("/filter", response_model=ApiResponse)
async def filter_teachers(body: teacher_type.FilterTeacherBody) -> ApiResponse:
    return teacher_controller.filterTeacher(body)


@router.post("/update", response_model=ApiResponse)
async def update(body: teacher_type.UpdateTeacherBody) -> ApiResponse:
    return teacher_controller.updateTeacher(body)


@router.post("/remove", response_model=ApiResponse)
async def remove(body: teacher_type.RemoveTeacherBody) -> ApiResponse:
    return teacher_controller.removeTeacher(body)
