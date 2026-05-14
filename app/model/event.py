from datetime import datetime

from db import insert_returning_last_id, run
from app.list_search import append_in, append_like, compact_datetimes, non_empty_strs
import app.type.event as event


def createEvent(body: event.CreateEventBody) -> dict | None:
    sql = (
        "INSERT INTO event (building_id, event_name, start_time, end_time, organizer, "
        "description) VALUES (%s, %s, %s, %s, %s, %s)"
    )
    params = [
        body.building_id,
        body.event_name,
        body.start_time,
        body.end_time,
        body.organizer,
        body.description,
    ]
    new_id = insert_returning_last_id(sql, params)
    return getEventByID(new_id)


def getEventByID(event_id: int) -> dict | None:
    sql = "SELECT * FROM event WHERE event_id = %s"
    params = [event_id]
    return run(sql, params, fetch="one")


def removeEventByID(event_id: int) -> dict:
    sql = "DELETE FROM event WHERE event_id = %s"
    params = [event_id]
    run(sql, params, commit=True)
    return {"event_id": event_id}


def listEvents() -> list[dict]:
    sql = "SELECT * FROM event"
    params: list = []
    return run(sql, params, fetch="all")


def searchEvents(
    building_name: str | None = None,
    event_name: str | None = None,
    organizer: str | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    if building_name not in (None, ""):
        clauses.append(
            "(building_id IN (SELECT building_id FROM building WHERE building_name LIKE %s))"
        )
        params.append(f"%{building_name}%")
    append_like(clauses, params, "event_name", event_name)
    append_like(clauses, params, "organizer", organizer)
    if not clauses:
        sql = "SELECT * FROM event ORDER BY event_id"
        result = run(sql, [], fetch="all")
    else:
        sql = f"SELECT * FROM event WHERE {' AND '.join(clauses)} ORDER BY event_id"
        result = run(sql, params, fetch="all")
    return result if result else []


def filterEvents(
    building_name: list[str] | None = None,
    event_name: list[str] | None = None,
    organizer: list[str] | None = None,
    start_time: list[datetime] | None = None,
    end_time: list[datetime] | None = None,
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
    en = non_empty_strs(event_name)
    append_in(clauses, params, "event_name", en)
    org = non_empty_strs(organizer)
    append_in(clauses, params, "organizer", org)
    st = compact_datetimes(start_time)
    append_in(clauses, params, "start_time", st)
    et = compact_datetimes(end_time)
    append_in(clauses, params, "end_time", et)
    if not clauses:
        sql = "SELECT * FROM event ORDER BY event_id"
        result = run(sql, [], fetch="all")
    else:
        sql = f"SELECT * FROM event WHERE {' AND '.join(clauses)} ORDER BY event_id"
        result = run(sql, params, fetch="all")
    return result if result else []


def updateEvent(body: event.UpdateEventBody) -> dict | None:
    set_parts: list[str] = []
    params: list = []
    if body.building_id is not None:
        set_parts.append("building_id = %s")
        params.append(body.building_id)
    if body.event_name is not None:
        set_parts.append("event_name = %s")
        params.append(body.event_name)
    if body.start_time is not None:
        set_parts.append("start_time = %s")
        params.append(body.start_time)
    if body.end_time is not None:
        set_parts.append("end_time = %s")
        params.append(body.end_time)
    if body.organizer is not None:
        set_parts.append("organizer = %s")
        params.append(body.organizer)
    if body.description is not None:
        set_parts.append("description = %s")
        params.append(body.description)
    if set_parts:
        params.append(body.event_id)
        sql = f"UPDATE event SET {','.join(set_parts)} WHERE event_id = %s"
        run(sql, params, commit=True)
    return getEventByID(body.event_id)
