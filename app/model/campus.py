from db import run
from app.list_search import append_in, append_like, non_empty_strs
import app.type.campus as campus


def createCampus(body: campus.CreateCampusBody) -> dict:
    sql = "INSERT INTO campus (campus_name, address) VALUES (%s, %s)"
    params = [body.campus_name, body.campus_address]
    run(sql, params, commit = True)
    return getCampusByName(body.campus_name)


def getCampusByName(campus_name: str) -> dict:
    sql = "SELECT * FROM campus WHERE campus_name = %s"
    params = [campus_name]
    return run(sql, params, fetch = "one")


def getCampusByID(campus_id: int) -> dict:
    sql = "SELECT * FROM campus WHERE campus_id = %s"
    params = [campus_id]
    return run(sql, params, fetch = "one")


def removeCampusByName(campus_name: str) -> dict:
    sql = "DELETE FROM campus WHERE campus_name = %s"
    params = [campus_name]
    run(sql, params, commit=True)
    return {"campus_name": campus_name}


def removeCampusByID(campus_id: int) -> dict:
    sql = "DELETE FROM campus WHERE campus_id = %s"
    params = [campus_id]
    run(sql, params, commit=True)
    return {"campus_id": campus_id}


def listCampus() -> list[dict]:
    sql = "SELECT * FROM campus"
    params = []
    return run(sql, params, fetch = "all")


def searchCampus(
    campus_name: str | None = None, campus_address: str | None = None
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    append_like(clauses, params, "campus_name", campus_name)
    append_like(clauses, params, "address", campus_address)
    if not clauses:
        sql = "SELECT * FROM campus ORDER BY campus_id"
        result = run(sql, [], fetch="all")
    else:
        sql = f"SELECT * FROM campus WHERE {' AND '.join(clauses)} ORDER BY campus_id"
        result = run(sql, params, fetch="all")
    return result if result else []


def filterCampus(
    campus_name: list[str] | None = None,
    campus_address: list[str] | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    ns = non_empty_strs(campus_name)
    ads = non_empty_strs(campus_address)
    append_in(clauses, params, "campus_name", ns)
    append_in(clauses, params, "address", ads)
    if not clauses:
        sql = "SELECT * FROM campus ORDER BY campus_id"
        result = run(sql, [], fetch="all")
    else:
        sql = f"SELECT * FROM campus WHERE {' AND '.join(clauses)} ORDER BY campus_id"
        result = run(sql, params, fetch="all")
    return result if result else []


def updateCampus(body: campus.UpdateCampusBody) -> dict | None:
    set_parts = []
    params = []
    if body.campus_name is not None:
        set_parts.append("campus_name = %s")
        params.append(body.campus_name)
    if body.campus_address is not None:
        set_parts.append("address = %s")
        params.append(body.campus_address)
    if set_parts:
        params.append(body.campus_id)
        sql = f"UPDATE campus SET {', '.join(set_parts)} WHERE campus_id = %s"
        run(sql, params, commit = True)
    return getCampusByID(body.campus_id)
