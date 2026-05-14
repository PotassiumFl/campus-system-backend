from db import run
from app.list_search import append_in, append_like, compact_floats, non_empty_strs
import app.type.course as course


def createCourse(body: course.CreateCourseBody) -> dict | None:
    sql = (
        "INSERT INTO course (course_id, course_name, credit, offering_department) "
        "VALUES (%s, %s, %s, %s)"
    )
    params = [
        body.course_id,
        body.course_name,
        body.credit,
        body.department,
    ]
    run(sql, params, commit = True)
    return getCourseByPrimaryKey(body.course_id)


def getCourseByPrimaryKey(course_id: str) -> dict | None:
    sql = "SELECT * FROM course WHERE course_id = %s"
    params = [course_id]
    return run(sql, params, fetch = "one")


def getCourseByName(course_name: str) -> list[dict]:
    sql = "SELECT * FROM course WHERE course_name = %s ORDER BY course_id"
    params = [course_name]
    result = run(sql, params, fetch = "all")
    return result if result else []


def removeCourseByPrimaryKey(course_id: str) -> dict:
    sql = "DELETE FROM course WHERE course_id = %s"
    params = [course_id]
    run(sql, params, commit = True)
    return {
        "course_id": course_id,
    }


def listCourses() -> list[dict]:
    sql = "SELECT * FROM course"
    params: list = []
    return run(sql, params, fetch = "all")


def listCourseByDepartment(offering_department: str) -> list[dict]:
    sql = (
        "SELECT * FROM course WHERE offering_department = %s "
        "ORDER BY course_id"
    )
    params = [offering_department]
    result = run(sql, params, fetch = "all")
    return result if result else []


def searchCourses(
    course_name: str | None = None,
    department: str | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    append_like(clauses, params, "course_name", course_name)
    append_like(clauses, params, "offering_department", department)
    if not clauses:
        sql = "SELECT * FROM course ORDER BY course_id"
        result = run(sql, [], fetch="all")
    else:
        where = " AND ".join(clauses)
        sql = f"SELECT * FROM course WHERE {where} ORDER BY course_id"
        result = run(sql, params, fetch="all")

    return result if result else []


def filterCourses(
    course_id: list[str] | None = None,
    course_name: list[str] | None = None,
    department: list[str] | None = None,
    credit: list[float] | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    append_in(clauses, params, "course_id", non_empty_strs(course_id))
    append_in(clauses, params, "course_name", non_empty_strs(course_name))
    append_in(clauses, params, "offering_department", non_empty_strs(department))
    append_in(clauses, params, "credit", compact_floats(credit))
    if not clauses:
        sql = "SELECT * FROM course ORDER BY course_id"
        result = run(sql, [], fetch="all")
    else:
        where = " AND ".join(clauses)
        sql = f"SELECT * FROM course WHERE {where} ORDER BY course_id"
        result = run(sql, params, fetch="all")

    return result if result else []


def updateCourse(body: course.UpdateCourseBody) -> dict | None:
    set_parts: list[str] = []
    params: list = []
    if body.course_name is not None:
        set_parts.append("course_name = %s")
        params.append(body.course_name)
    if body.credit is not None:
        set_parts.append("credit = %s")
        params.append(body.credit)
    if body.department is not None:
        set_parts.append("offering_department = %s")
        params.append(body.department)
    if set_parts:
        params.append(body.course_id)
        sql = (
            f"UPDATE course SET {','.join(set_parts)} "
            "WHERE course_id = %s"
        )
        run(sql, params, commit = True)
    return getCourseByPrimaryKey(body.course_id)
