from starlette import status

import app.model.course as course
import app.type.course as course_type
from app.type.response import ApiResponse


def uploadCourse(body: course_type.UploadCourseBody) -> ApiResponse:
    created = course.createCourse(
        course_type.CreateCourseBody(
            course_id=body.course_id,
            course_name=body.course_name,
            credit=body.credit,
            department=body.department,
        )
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_201_CREATED,
        message=None,
        data=created,
    )


def searchCourse(body: course_type.SearchCourseBody) -> ApiResponse:
    rows = course.searchCourses(
        course_name=body.course_name,
        department=body.department,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=rows,
    )


def filterCourse(body: course_type.FilterCourseBody) -> ApiResponse:
    rows = course.filterCourses(
        course_id=body.course_id,
        course_name=body.course_name,
        department=body.department,
        credit=body.credit,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=rows,
    )


def updateCourse(body: course_type.UpdateCourseBody) -> ApiResponse:
    existing = course.getCourseByPrimaryKey(body.course_id)
    if existing is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Course not found",
            data=None,
        )
    if body.course_name is None and body.credit is None and body.department is None:
        return ApiResponse(
            success=True,
            code=status.HTTP_200_OK,
            message=None,
            data=existing,
        )
    updated = course.updateCourse(body)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=updated,
    )


def removeCourse(body: course_type.RemoveCourseBody) -> ApiResponse:
    if course.getCourseByPrimaryKey(body.course_id) is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Course not found",
            data=None,
        )
    removed = course.removeCourseByPrimaryKey(body.course_id)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=removed,
    )
