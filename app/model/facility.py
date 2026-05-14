from db import run
from app.list_search import append_in, append_like, non_empty_strs
import app.type.facility as facility


def createFacility(body: facility.CreateFacilityBody) -> dict:
    sql = "INSERT INTO facility (building_id, facility_name, facility_type, open_time) VALUES (%s, %s, %s, %s)"
    params = [body.building_id, body.facility_name, body.facility_type.value, body.openTime]
    run(sql, params, commit = True)
    return getFacilityByName(body.facility_name)


def getFacilityByName(facility_name: str) -> dict:
    sql = "SELECT * FROM facility WHERE facility_name = %s"
    params = [facility_name]
    return run(sql, params, fetch = "one")


def getFacilityByID(facility_id: int) -> dict:
    sql = "SELECT * FROM facility WHERE facility_id = %s"
    params = [facility_id]
    return run(sql, params, fetch = "one")


def removeFacilityByID(facility_id: int) -> dict:
    sql = "DELETE FROM facility WHERE facility_id = %s"
    params = [facility_id]
    run(sql, params, commit=True)
    return {"facility_id": facility_id}


def listFacilities() -> list[dict]:
    sql = "SELECT * FROM facility"
    params = []
    return run(sql, params, fetch = "all")


def searchFacilities(
    building_name: str | None = None,
    facility_name: str | None = None,
    open_time: str | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    if building_name not in (None, ""):
        clauses.append(
            "(building_id IN (SELECT building_id FROM building WHERE building_name LIKE %s))"
        )
        params.append(f"%{building_name}%")
    append_like(clauses, params, "facility_name", facility_name)
    append_like(clauses, params, "open_time", open_time)
    if not clauses:
        sql = "SELECT * FROM facility ORDER BY facility_id"
        result = run(sql, [], fetch="all")
    else:
        sql = f"SELECT * FROM facility WHERE {' AND '.join(clauses)} ORDER BY facility_id"
        result = run(sql, params, fetch="all")
    return result if result else []


def filterFacilities(
    building_name: list[str] | None = None,
    facility_name: list[str] | None = None,
    facility_type: list[facility.FacilityType] | None = None,
    open_time: list[str] | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    bn = non_empty_strs(building_name)
    if bn:
        ph = ", ".join(["%s"] * len(bn))
        clauses.append(
            "(building_id IN (SELECT building_id FROM building WHERE building_name IN ("
            f"{ph})))"
        )
        params.extend(bn)
    fn = non_empty_strs(facility_name)
    append_in(clauses, params, "facility_name", fn)
    ft_vals = [t.value for t in (facility_type or []) if t is not None]
    append_in(clauses, params, "facility_type", ft_vals)
    ot = non_empty_strs(open_time)
    append_in(clauses, params, "open_time", ot)
    if not clauses:
        sql = "SELECT * FROM facility ORDER BY facility_id"
        result = run(sql, [], fetch="all")
    else:
        sql = f"SELECT * FROM facility WHERE {' AND '.join(clauses)} ORDER BY facility_id"
        result = run(sql, params, fetch="all")
    return result if result else []


def updateFacility(body: facility.UpdateFacilityBody) -> dict:
    set_parts = []
    params = []
    if body.facility_name is not None:
        set_parts.append("facility_name = %s")
        params.append(body.facility_name)
    if body.building_id is not None:
        set_parts.append("building_id = %s")
        params.append(body.building_id)
    if body.facility_type is not None:
        set_parts.append("facility_type = %s")
        params.append(body.facility_type.value)
    if body.openTime is not None:
        set_parts.append("open_time = %s")
        params.append(body.openTime)
    if set_parts:
        params.append(body.facility_id)
        sql = f"UPDATE facility SET {','.join(set_parts)} WHERE facility_id = %s"
        run(sql, params, commit = True)
    return getFacilityByID(body.facility_id)
