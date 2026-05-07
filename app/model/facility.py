from db import run
import app.type.facility as facility


def createFacility(body: facility.CreateFacilityBody) -> dict:
    sql = "INSERT INTO facility (building_id, facility_name, facility_type, open_time) VALUES (%s, %s, %s, %s)"
    params = [body.building_id, body.name, body.type.value, body.openTime]
    run(sql, params, commit = True)
    return getFacilityByName(body.name)


def getFacilityByName(name: str) -> dict:
    sql = "SELECT * FROM facility WHERE facility_name = %s"
    params = [name]
    return run(sql, params, fetch = "one")


def getFacilityByID(id: int) -> dict:
    sql = "SELECT * FROM facility WHERE facility_id = %s"
    params = [id]
    return run(sql, params, fetch = "one")


def removeFacilityByID(id: int) -> dict:
    sql = "DELETE FROM facility WHERE facility_id = %s"
    params = [id]
    run(sql, params)
    return {"id": id}


def listFacilities() -> list[dict]:
    sql = "SELECT * FROM facility"
    params = []
    return run(sql, params, fetch = "all")


def updateFacility(body: facility.UpdateFacilityBody) -> dict:
    set_parts = []
    params = []
    if body.name is not None:
        set_parts.append("facility_name = %s")
        params.append(body.name)
    if body.building_id is not None:
        set_parts.append("building_id = %s")
        params.append(body.building_id)
    if body.type is not None:
        set_parts.append("facility_type = %s")
        params.append(body.type.value)
    if body.openTime is not None:
        set_parts.append("open_time = %s")
        params.append(body.openTime)
    if set_parts:
        params.append(body.id)
        sql = f"UPDATE facility SET {','.join(set_parts)} WHERE facility_id = %s"
        run(sql, params, commit = True)
    return getFacilityByID(body.id)
