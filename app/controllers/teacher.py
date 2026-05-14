from starlette import status

import app.model.teacher as teacher
import app.type.teacher as teacher_type
from app.type.response import ApiResponse


def uploadTeacher(body: teacher_type.UploadTeacherBody) -> ApiResponse:
    created = teacher.createTeacher(
        teacher_type.CreateTeacherBody(
            teacher_name=body.teacher_name,
            department=body.department,
            email=body.email,
        )
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_201_CREATED,
        message=None,
        data=created,
    )


def searchTeacher(body: teacher_type.SearchTeacherBody) -> ApiResponse:
    rows = teacher.searchTeachers(
        teacher_name=body.teacher_name,
        department=body.department,
        email=body.email,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=rows,
    )


def filterTeacher(body: teacher_type.FilterTeacherBody) -> ApiResponse:
    rows = teacher.filterTeachers(
        teacher_name=body.teacher_name,
        department=body.department,
        email=body.email,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=rows,
    )


def updateTeacher(body: teacher_type.UpdateTeacherBody) -> ApiResponse:
    existing = teacher.getTeacherByID(body.teacher_id)
    if existing is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Teacher not found",
            data=None,
        )
    if body.email is not None:
        other = teacher.getTeacherByEmail(body.email)
        if other is not None and other["teacher_id"] != body.teacher_id:
            return ApiResponse(
                success=False,
                code=status.HTTP_409_CONFLICT,
                message="Email already in use",
                data=None,
            )
    if (
        body.teacher_name is None
        and body.department is None
        and body.email is None
    ):
        return ApiResponse(
            success=True,
            code=status.HTTP_200_OK,
            message=None,
            data=existing,
        )
    updated = teacher.updateTeacher(body)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=updated,
    )


def removeTeacher(body: teacher_type.RemoveTeacherBody) -> ApiResponse:
    if teacher.getTeacherByID(body.teacher_id) is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Teacher not found",
            data=None,
        )
    removed = teacher.removeTeacherByID(body.teacher_id)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=removed,
    )
