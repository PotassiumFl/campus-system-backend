from starlette import status

import app.model.teach as teach_model
import app.type.teach as teach_type
from app.type.response import ApiResponse


def uploadTeach(body: teach_type.UploadTeachBody) -> ApiResponse:
    role = body.role if body.role is not None else teach_type.TeachRole.teacher
    created = teach_model.createTeach(
        teach_type.CreateTeachBody(
            teacher_id=body.teacher_id,
            course_id=body.course_id,
            semester=body.semester,
            section_no=body.section_no,
            role=role,
            start_time=body.start_time,
            end_time=body.end_time,
        )
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_201_CREATED,
        message=None,
        data=created,
    )


def updateTeach(body: teach_type.UpdateTeachBody) -> ApiResponse:
    existing = teach_model.getTeachByPrimaryKey(
        body.teacher_id,
        body.course_id,
        body.semester,
        body.section_no,
    )
    if existing is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Teach record not found",
            data=None,
        )
    if body.role is None and body.start_time is None and body.end_time is None:
        return ApiResponse(
            success=True,
            code=status.HTTP_200_OK,
            message=None,
            data=existing,
        )
    updated = teach_model.updateTeach(body)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=updated,
    )


def searchTeach(body: teach_type.SearchTeachBody) -> ApiResponse:
    rows = teach_model.searchTeach(
        semester=body.semester,
        section_no=body.section_no,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=rows,
    )


def filterTeach(body: teach_type.FilterTeachBody) -> ApiResponse:
    rows = teach_model.filterTeach(
        teacher_id=body.teacher_id,
        course_id=body.course_id,
        semester=body.semester,
        section_no=body.section_no,
        role=body.role,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=rows,
    )


def removeTeach(body: teach_type.RemoveTeachBody) -> ApiResponse:
    if (
        teach_model.getTeachByPrimaryKey(
            body.teacher_id,
            body.course_id,
            body.semester,
            body.section_no,
        )
        is None
    ):
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Teach record not found",
            data=None,
        )
    removed = teach_model.removeTeachByPrimaryKey(
        body.teacher_id,
        body.course_id,
        body.semester,
        body.section_no,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=removed,
    )
