from db import insert_returning_last_id, run
from app.list_search import append_in, append_like, compact_ints, non_empty_strs
import app.type.queryRecord as query_record


def createQueryRecord(body: query_record.CreateQueryRecordBody) -> dict | None:
    sql = (
        "INSERT INTO query_record (user_id, query_type, query_text, answer) "
        "VALUES (%s, %s, %s, %s)"
    )
    params = [body.user_id, body.query_type.value, body.query_text, body.answer]
    new_id = insert_returning_last_id(sql, params)
    return getQueryRecordByID(new_id)


def getQueryRecordByID(id: int) -> dict | None:
    sql = "SELECT * FROM query_record WHERE record_id = %s"
    params = [id]
    return run(sql, params, fetch="one")


def removeQueryRecordByID(id: int) -> dict:
    sql = "DELETE FROM query_record WHERE record_id = %s"
    params = [id]
    run(sql, params, commit=True)
    return {"id": id}


def listQueryRecords() -> list[dict]:
    sql = "SELECT * FROM query_record"
    params: list = []
    return run(sql, params, fetch="all")


def listQueryRecordsByUserId(user_id: int) -> list[dict]:
    sql = "SELECT * FROM query_record WHERE user_id = %s ORDER BY query_time DESC"
    params = [user_id]
    return run(sql, params, fetch="all")


def updateQueryRecord(body: query_record.UpdateQueryRecordBody) -> dict | None:
    set_parts: list[str] = []
    params: list = []
    if body.user_id is not None:
        set_parts.append("user_id = %s")
        params.append(body.user_id)
    if body.query_type is not None:
        set_parts.append("query_type = %s")
        params.append(body.query_type.value)
    if body.query_text is not None:
        set_parts.append("query_text = %s")
        params.append(body.query_text)
    if body.answer is not None:
        set_parts.append("answer = %s")
        params.append(body.answer)
    if set_parts:
        params.append(body.id)
        sql = f"UPDATE query_record SET {','.join(set_parts)} WHERE record_id = %s"
        run(sql, params, commit=True)
    return getQueryRecordByID(body.id)


def searchQueryRecords(
    user_id: int | None = None,
    query_text: str | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    if user_id is not None:
        clauses.append("(user_id = %s)")
        params.append(user_id)
    append_like(clauses, params, "query_text", query_text)
    if not clauses:
        sql = "SELECT * FROM query_record ORDER BY record_id DESC"
        result = run(sql, [], fetch="all")
    else:
        sql = f"SELECT * FROM query_record WHERE {' AND '.join(clauses)} ORDER BY record_id DESC"
        result = run(sql, params, fetch="all")
    return result if result else []


def filterQueryRecords(
    user_id: list[int] | None = None,
    query_type: list[str] | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list = []
    append_in(clauses, params, "user_id", compact_ints(user_id))
    append_in(clauses, params, "query_type", non_empty_strs(query_type))
    if not clauses:
        sql = "SELECT * FROM query_record ORDER BY record_id DESC"
        result = run(sql, [], fetch="all")
    else:
        sql = f"SELECT * FROM query_record WHERE {' AND '.join(clauses)} ORDER BY record_id DESC"
        result = run(sql, params, fetch="all")
    return result if result else []
