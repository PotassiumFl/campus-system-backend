from starlette import status

import app.model.course as course_model
import app.model.teach as teach_model
import app.model.teacher as teacher_model
import app.type.teach as teach_type
from app.type.response import ApiResponse


def _resolve_teacher_ids(teacher_name: str | None) -> list[int] | None:
    if teacher_name in (None, ""):
        return None
    rows = teacher_model.searchTeachers(teacher_name=teacher_name)
    return [row["teacher_id"] for row in rows]


def _resolve_course_ids(
    course_id: str | None,
    course_name: str | None,
) -> list[str] | None:
    if course_id not in (None, ""):
        return [course_id]
    if course_name in (None, ""):
        return None
    rows = course_model.searchCourses(course_name=course_name)
    return [row["course_id"] for row in rows]


def _merge_teach_rows(rows_list: list[list[dict]]) -> list[dict]:
    merged: list[dict] = []
    seen: set[tuple] = set()
    for rows in rows_list:
        for row in rows:
            key = (
                row["teacher_id"],
                row["course_id"],
                row["semester"],
                row["section_no"],
            )
            if key in seen:
                continue
            seen.add(key)
            merged.append(row)
    return merged


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
    teacher_ids = _resolve_teacher_ids(body.teacher_name)
    course_ids = _resolve_course_ids(body.course_id, body.course_name)

    if body.teacher_name and not teacher_ids:
        rows: list[dict] = []
    elif body.course_name and body.course_id in (None, "") and not course_ids:
        rows = []
    elif teacher_ids and course_ids:
        batch: list[list[dict]] = []
        for teacher_id in teacher_ids:
            for course_id in course_ids:
                batch.append(
                    teach_model.searchTeach(
                        semester=body.semester,
                        section_no=body.section_no,
                        teacher_id=teacher_id,
                        course_id=course_id,
                    )
                )
        rows = _merge_teach_rows(batch)
    elif teacher_ids:
        batch = [
            teach_model.searchTeach(
                semester=body.semester,
                section_no=body.section_no,
                teacher_id=teacher_id,
                course_id=body.course_id,
            )
            for teacher_id in teacher_ids
        ]
        rows = _merge_teach_rows(batch)
    elif course_ids:
        batch = [
            teach_model.searchTeach(
                semester=body.semester,
                section_no=body.section_no,
                course_id=course_id,
            )
            for course_id in course_ids
        ]
        rows = _merge_teach_rows(batch)
    else:
        rows = teach_model.searchTeach(
            semester=body.semester,
            section_no=body.section_no,
            course_id=body.course_id,
        )

    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=rows,
    )


def filterTeach(body: teach_type.FilterTeachBody) -> ApiResponse:
    teacher_ids = _resolve_teacher_ids(body.teacher_name)
    if body.teacher_name and not teacher_ids:
        rows = []
    else:
        course_ids = _resolve_course_ids(None, body.course_name)
        if body.course_name and not course_ids:
            rows = []
        else:
            semester = [body.semester] if body.semester not in (None, "") else None
            rows = teach_model.filterTeach(
                teacher_id=teacher_ids,
                course_id=course_ids,
                semester=semester,
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
