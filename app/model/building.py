from db import run
from app.list_search import append_in, append_like, non_empty_strs
import app.type.building as building


def createBuilding(body: building.CreateBuildingBody) -> dict:
    sql = "INSERT INTO building (campus_id, building_name, building_type) VALUES (%s, %s, %s)"
    params = [body.campus_id, body.building_name, body.building_type.value]
    run(sql, params, commit = True)
    return getBuildingByName(body.building_name)

def getBuildingByName(building_name: str) -> dict:
    sql = "SELECT * FROM building WHERE building_name = %s"
    params = [building_name]
    return run(sql, params, fetch = "one")


def getBuildingByID(building_id: int) -> dict:
    sql = "SELECT * FROM building WHERE building_id = %s"
    params = [building_id]
    return run(sql, params, fetch = "one")

def removeBuildingByName(building_name: str) -> dict:
    sql = "DELETE FROM building WHERE building_name = %s"
    params = [building_name]
    run(sql, params, commit=True)
    return {"building_name": name}


def removeBuildingByID(building_id: int) -> dict:
    sql = "DELETE FROM building WHERE building_id = %s"
    params = [building_id]
    run(sql, params, commit=True)
    return {"building_id": building_id}

def listBuildings() -> list[dict]:
    sql = "SELECT * FROM building"
    params = []
    return run(sql, params, fetch = "all")


def searchBuildings(
    campus_name: str | None = None,
    building_name: str | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    if campus_name not in (None, ""):
        clauses.append(
            "(campus_id IN (SELECT campus_id FROM campus WHERE campus_name LIKE %s))"
        )
        params.append(f"%{campus_name}%")
    append_like(clauses, params, "building_name", building_name)
    if not clauses:
        sql = "SELECT * FROM building ORDER BY building_id"
        result = run(sql, [], fetch="all")
    else:
        sql = f"SELECT * FROM building WHERE {' AND '.join(clauses)} ORDER BY building_id"
        result = run(sql, params, fetch="all")
    return result if result else []


def filterBuildings(
    campus_name: list[str] | None = None,
    building_name: list[str] | None = None,
    building_type: list[building.BuildingType] | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    cn = non_empty_strs(campus_name)
    if cn:
        ph = ", ".join(["%s"] * len(cn))
        clauses.append(
            "(campus_id IN (SELECT campus_id FROM campus WHERE campus_name IN ("
            f"{ph})))"
        )
        params.extend(cn)
    bn = non_empty_strs(building_name)
    append_in(clauses, params, "building_name", bn)
    bt_vals = [t.value for t in (building_type or []) if t is not None]
    append_in(clauses, params, "building_type", bt_vals)
    if not clauses:
        sql = "SELECT * FROM building ORDER BY building_id"
        result = run(sql, [], fetch="all")
    else:
        sql = f"SELECT * FROM building WHERE {' AND '.join(clauses)} ORDER BY building_id"
        result = run(sql, params, fetch="all")
    return result if result else []


def updateBuilding(body: building.UpdateBuildingBody) -> dict | None:
    set_parts = []
    params = []
    if body.building_name is not None:
        set_parts.append("building_name = %s")
        params.append(body.building_name)
    if body.campus_id is not None:
        set_parts.append("campus_id = %s")
        params.append(body.campus_id)
    if body.building_type is not None:
        set_parts.append("building_type = %s")
        params.append(body.building_type.value)
    if set_parts:
        params.append(body.building_id)
        sql = f"UPDATE building SET {','.join(set_parts)} WHERE building_id = %s"
        run(sql, params, commit = True)
    return getBuildingByID(body.building_id)
