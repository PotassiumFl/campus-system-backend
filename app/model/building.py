from db import run
import app.type.building as building


def createBuilding(body: building.CreateBuildingBody) -> dict:
    sql = "INSERT INTO building (campus_id, building_name, building_type) VALUES (%s, %s, %s)"
    params = [body.campus_id, body.name, body.type.value]
    run(sql, params, commit = True)
    return getBuildingByName(body.name)

def getBuildingByName(name: str) -> dict:
    sql = "SELECT * FROM building WHERE building_name = %s"
    params = [name]
    return run(sql, params, fetch = "one")


def getBuildingByID(id: int) -> dict:
    sql = "SELECT * FROM building WHERE building_id = %s"
    params = [id]
    return run(sql, params, fetch = "one")

def removeBuildingByName(name: str) -> dict:
    sql = "DELETE FROM building WHERE building_name = %s"
    params = [name]
    run(sql, params)
    return {"name": name}

def listBuildings() -> list[dict]:
    sql = "SELECT * FROM building"
    params = []
    return run(sql, params, fetch = "all")

def updateBuilding(body: building.UpdateBuildingBody) -> dict | None:
    set_parts = []
    params = []
    if body.name is not None:
        set_parts.append("building_name = %s")
        params.append(body.name)
    if body.campus_id is not None:
        set_parts.append("campus_id = %s")
        params.append(body.campus_id)
    if body.type is not None:
        set_parts.append("building_type = %s")
        params.append(body.type.value)
    if set_parts:
        params.append(body.id)
        sql = f"UPDATE building SET {','.join(set_parts)} WHERE building_id = %s"
        run(sql, params, commit = True)
    return getBuildingByID(body.id)
