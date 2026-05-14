from fastapi import APIRouter, status

from app.controllers import course as course_controller
from app.type import course as course_type
from app.type.response import ApiResponse

router = APIRouter()


@router.post("/upload", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def upload(body: course_type.UploadCourseBody) -> ApiResponse:
    return course_controller.uploadCourse(body)


@router.post("/search", response_model=ApiResponse)
async def search(body: course_type.SearchCourseBody) -> ApiResponse:
    return course_controller.searchCourse(body)


@router.post("/filter", response_model=ApiResponse)
async def filter_courses(body: course_type.FilterCourseBody) -> ApiResponse:
    return course_controller.filterCourse(body)


@router.post("/update", response_model=ApiResponse)
async def update(body: course_type.UpdateCourseBody) -> ApiResponse:
    return course_controller.updateCourse(body)


@router.post("/remove", response_model=ApiResponse)
async def remove(body: course_type.RemoveCourseBody) -> ApiResponse:
    return course_controller.removeCourse(body)
