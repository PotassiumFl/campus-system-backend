from db import run
from app.list_search import append_in, append_like, compact_ints, non_empty_strs
import app.type.teach as teach

_TEACH_SELECT = (
    "SELECT t.*, tr.teacher_name, c.course_name, c.credit "
    "FROM teach t "
    "LEFT JOIN teacher tr ON t.teacher_id = tr.teacher_id "
    "LEFT JOIN course c ON t.course_id = c.course_id"
)
_TEACH_ORDER = " ORDER BY t.semester, t.section_no, t.course_id, t.teacher_id"


def createTeach(body: teach.CreateTeachBody) -> dict | None:
    sql = (
        "INSERT INTO teach (teacher_id, course_id, semester, section_no, teach_role, start_time, end_time) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )
    params = [
        body.teacher_id,
        body.course_id,
        body.semester,
        body.section_no,
        body.role.value,
        body.start_time,
        body.end_time,
    ]
    run(sql, params, commit=True)
    return getTeachByPrimaryKey(
        body.teacher_id,
        body.course_id,
        body.semester,
        body.section_no,
    )


def getTeachByPrimaryKey(
    teacher_id: int,
    course_id: str,
    semester: str,
    section_no: str,
) -> dict | None:
    sql = (
        f"{_TEACH_SELECT} WHERE t.teacher_id = %s AND t.course_id = %s "
        "AND t.semester = %s AND t.section_no = %s"
    )
    params = [teacher_id, course_id, semester, section_no]
    return run(sql, params, fetch="one")


def searchTeach(
    semester: str | None = None,
    section_no: str | None = None,
    teacher_id: int | None = None,
    course_id: str | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    if teacher_id is not None:
        clauses.append("(t.teacher_id = %s)")
        params.append(teacher_id)
    if course_id not in (None, ""):
        clauses.append("(t.course_id = %s)")
        params.append(course_id)
    append_like(clauses, params, "t.semester", semester)
    append_like(clauses, params, "t.section_no", section_no)
    if not clauses:
        sql = f"{_TEACH_SELECT}{_TEACH_ORDER}"
        result = run(sql, [], fetch="all")
    else:
        sql = f"{_TEACH_SELECT} WHERE {' AND '.join(clauses)}{_TEACH_ORDER}"
        result = run(sql, params, fetch="all")
    return result if result else []


def filterTeach(
    teacher_id: list[int] | None = None,
    course_id: list[str] | None = None,
    semester: list[str] | None = None,
    section_no: list[str] | None = None,
    role: list[teach.TeachRole] | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    append_in(clauses, params, "t.teacher_id", compact_ints(teacher_id))
    append_in(clauses, params, "t.course_id", non_empty_strs(course_id))
    append_in(clauses, params, "t.semester", non_empty_strs(semester))
    append_in(clauses, params, "t.section_no", non_empty_strs(section_no))
    role_vals = [r.value for r in (role or []) if r is not None]
    append_in(clauses, params, "t.teach_role", role_vals)
    if not clauses:
        sql = f"{_TEACH_SELECT}{_TEACH_ORDER}"
        result = run(sql, [], fetch="all")
    else:
        sql = f"{_TEACH_SELECT} WHERE {' AND '.join(clauses)}{_TEACH_ORDER}"
        result = run(sql, params, fetch="all")
    return result if result else []


def removeTeachByPrimaryKey(
    teacher_id: int,
    course_id: str,
    semester: str,
    section_no: str,
) -> dict:
    sql = (
        "DELETE FROM teach WHERE teacher_id = %s AND course_id = %s "
        "AND semester = %s AND section_no = %s"
    )
    params = [teacher_id, course_id, semester, section_no]
    run(sql, params, commit=True)
    return {
        "teacher_id": teacher_id,
        "course_id": course_id,
        "semester": semester,
        "section_no": section_no,
    }


def updateTeach(body: teach.UpdateTeachBody) -> dict | None:
    set_parts: list[str] = []
    params: list = []
    if body.role is not None:
        set_parts.append("teach_role = %s")
        params.append(body.role.value)
    if body.start_time is not None:
        set_parts.append("start_time = %s")
        params.append(body.start_time)
    if body.end_time is not None:
        set_parts.append("end_time = %s")
        params.append(body.end_time)
    if set_parts:
        params.extend(
            [
                body.teacher_id,
                body.course_id,
                body.semester,
                body.section_no,
            ]
        )
        sql = (
            f"UPDATE teach SET {','.join(set_parts)} "
            "WHERE teacher_id = %s AND course_id = %s AND semester = %s AND section_no = %s"
        )
        run(sql, params, commit=True)
    return getTeachByPrimaryKey(
        body.teacher_id,
        body.course_id,
        body.semester,
        body.section_no,
    )