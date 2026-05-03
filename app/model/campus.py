from db import run
import app.type.campus as campus


def createCampus(body: campus.CreateCampusBody) -> dict:
    sql = "INSERT INTO campus (campus_name, address) VALUES (%s, %s)"
    params = [body.name, body.address]
    run(sql, params, commit = True)
    return getCampusByName(body.name)


def getCampusByName(name: str) -> dict:
    sql = "SELECT * FROM campus WHERE campus_name = %s"
    params = [name]
    return run(sql, params, fetch = "one")


def getCampusByID(id: int) -> dict:
    sql = "SELECT * FROM campus WHERE campus_id = %s"
    params = [id]
    return run(sql, params, fetch = "one")


def removeCampusByName(name: str) -> dict:
    sql = "DELETE FROM campus WHERE campus_name = %s"
    params = [name]
    run(sql, params)
    return {"name": name}


def listCampus() -> list[dict]:
    sql = "SELECT * FROM campus"
    params = []
    return run(sql, params, fetch = "all")


def updateCampus(body: campus.UpdateCampusBody) -> dict | None:
    set_parts: list[str] = []
    params: list = []
    if body.name is not None:
        set_parts.append("campus_name = %s")
        params.append(body.name)
    if body.address is not None:
        set_parts.append("address = %s")
        params.append(body.address)
    if set_parts:
        params.append(body.id)
        sql = f"UPDATE campus SET {', '.join(set_parts)} WHERE campus_id = %s"
        run(sql, params, commit = True)
    return getCampusByID(body.id)
