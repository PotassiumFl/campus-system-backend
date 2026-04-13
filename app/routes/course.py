from fastapi import APIRouter, HTTPException
from starlette import status

from app.schemas.models import ApiResponse, searchCourseBody, uploadCourseBody
from db.course_repository import course_id_exists, insert_course, search_course, course_exists

router = APIRouter()


@router.post("/course/search", response_model=ApiResponse, status_code=status.HTTP_200_OK)
async def course_search(body: searchCourseBody) -> ApiResponse:
    courses = search_course(body)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=courses,
    )


@router.post("/course/upload", response_model = ApiResponse, status_code = status.HTTP_201_CREATED)
async def course_upload(body: uploadCourseBody) -> ApiResponse:
    if course_exists(body):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="course already exists",
        )
    insert_course(body)
    return ApiResponse(
        success = True,
        code = status.HTTP_201_CREATED,
        message = "course uploaded",
        data = None
    )