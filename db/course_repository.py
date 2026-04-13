from app.schemas.models import CourseBody, searchCourseBody, uploadCourseBody
from db.connection import get_connection


def insert_course(body: uploadCourseBody) -> bool:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO course (`C#`, CNAME, CREDIT, DEPARTMENT, SEMESTER) VALUES (%s, %s, %s, %s, %s)",
                (body.course_id, body.course_name, body.credit, body.department, body.semester),
            )
        conn.commit()
        return True
    finally:
        conn.close()


def course_id_exists(course_id: str) -> bool:
    """Same primary key as an existing row (matches DB uniqueness on `C#`)."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM course WHERE `C#` = %s LIMIT 1", (course_id,))
            return cur.fetchone() is not None
    finally:
        conn.close()


def course_exists(body: CourseBody) -> bool:
    """True only if all columns match the given body (stricter than primary key)."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM course WHERE `C#` = %s AND CNAME = %s AND CREDIT = %s AND DEPARTMENT = %s AND SEMESTER = %s LIMIT 1",
                (body.course_id, body.course_name, body.credit, body.department, body.semester),
            )
            return cur.fetchone() is not None
    finally:
        conn.close()


def search_course(body: searchCourseBody) -> list[CourseBody]:
    conditions: list[str] = []
    params: list = []
    if body.course_id:
        ph = ",".join(["%s"] * len(body.course_id))
        conditions.append(f"`C#` IN ({ph})")
        params.extend(body.course_id)
    if body.course_name:
        ph = ",".join(["%s"] * len(body.course_name))
        conditions.append(f"CNAME IN ({ph})")
        params.extend(body.course_name)
    if body.credit:
        ph = ",".join(["%s"] * len(body.credit))
        conditions.append(f"CREDIT IN ({ph})")
        params.extend(body.credit)
    if body.department:
        ph = ",".join(["%s"] * len(body.department))
        conditions.append(f"DEPARTMENT IN ({ph})")
        params.extend(body.department)
    if body.semester:
        ph = ",".join(["%s"] * len(body.semester))
        conditions.append(f"SEMESTER IN ({ph})")
        params.extend(body.semester)

    sql = "SELECT `C#`, CNAME, CREDIT, DEPARTMENT, SEMESTER FROM course"
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(params) if params else None)
            rows = cur.fetchall()
        return [
            CourseBody(
                course_id=row[0],
                course_name=row[1],
                credit=float(row[2]),
                department=row[3],
                semester=row[4],
            )
            for row in rows
        ]
    finally:
        conn.close()


