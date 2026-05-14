from db import insert_returning_last_id, run
from app.list_search import append_in, append_like, non_empty_strs
import app.type.teacher as teacher


def createTeacher(body: teacher.CreateTeacherBody) -> dict | None:
    sql = (
        "INSERT INTO teacher (teacher_name, department, email) VALUES (%s, %s, %s)"
    )
    params = [body.teacher_name, body.department, body.email]
    new_id = insert_returning_last_id(sql, params)
    return getTeacherByID(new_id)


def getTeacherByID(teacher_id: int) -> dict | None:
    sql = "SELECT * FROM teacher WHERE teacher_id = %s"
    params = [teacher_id]
    return run(sql, params, fetch="one")


def getTeacherByEmail(email: str) -> dict | None:
    sql = "SELECT * FROM teacher WHERE email = %s"
    params = [email]
    return run(sql, params, fetch="one")


def removeTeacherByID(teacher_id: int) -> dict:
    sql = "DELETE FROM teacher WHERE teacher_id = %s"
    params = [teacher_id]
    run(sql, params, commit=True)
    return {"teacher_id": teacher_id}


def removeTeacherByEmail(email: str) -> dict:
    sql = "DELETE FROM teacher WHERE email = %s"
    params = [email]
    run(sql, params, commit=True)
    return {"email": email}


def listTeachers() -> list[dict]:
    sql = "SELECT * FROM teacher"
    params: list = []
    return run(sql, params, fetch="all")


def searchTeachers(
    teacher_name: str | None = None,
    department: str | None = None,
    email: str | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    append_like(clauses, params, "teacher_name", teacher_name)
    append_like(clauses, params, "department", department)
    append_like(clauses, params, "email", email)
    if not clauses:
        sql = "SELECT * FROM teacher ORDER BY teacher_id"
        result = run(sql, [], fetch="all")
    else:
        sql = f"SELECT * FROM teacher WHERE {' AND '.join(clauses)} ORDER BY teacher_id"
        result = run(sql, params, fetch="all")
    return result if result else []


def filterTeachers(
    teacher_name: list[str] | None = None,
    department: list[str] | None = None,
    email: list[str] | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    ns = non_empty_strs(teacher_name)
    append_in(clauses, params, "teacher_name", ns)
    ds = non_empty_strs(department)
    append_in(clauses, params, "department", ds)
    es = non_empty_strs(email)
    append_in(clauses, params, "email", es)
    if not clauses:
        sql = "SELECT * FROM teacher ORDER BY teacher_id"
        result = run(sql, [], fetch="all")
    else:
        sql = f"SELECT * FROM teacher WHERE {' AND '.join(clauses)} ORDER BY teacher_id"
        result = run(sql, params, fetch="all")
    return result if result else []


def updateTeacher(body: teacher.UpdateTeacherBody) -> dict | None:
    set_parts: list[str] = []
    params: list = []
    if body.teacher_name is not None:
        set_parts.append("teacher_name = %s")
        params.append(body.teacher_name)
    if body.department is not None:
        set_parts.append("department = %s")
        params.append(body.department)
    if body.email is not None:
        set_parts.append("email = %s")
        params.append(body.email)
    if set_parts:
        params.append(body.teacher_id)
        sql = f"UPDATE teacher SET {','.join(set_parts)} WHERE teacher_id = %s"
        run(sql, params, commit=True)
    return getTeacherByID(body.teacher_id)
