from starlette import status

import app.model.query_record as query_record_model
import app.type.queryRecord as query_record_type
from app.type.response import ApiResponse


def _as_public_record(row: dict | None) -> dict | None:
    if row is None:
        return None
    out = dict(row)
    if "record_id" in out:
        out["id"] = out.pop("record_id")
    return out


def _as_public_records(rows: list[dict]) -> list[dict]:
    return [_as_public_record(row) for row in rows if row is not None]  # type: ignore[misc]


def uploadQueryRecord(body: query_record_type.CreateQueryRecordBody) -> ApiResponse:
    created = query_record_model.createQueryRecord(body)
    return ApiResponse(
        success=True,
        code=status.HTTP_201_CREATED,
        message=None,
        data=_as_public_record(created),
    )


def searchQueryRecord(body: query_record_type.SearchQueryRecordBody) -> ApiResponse:
    rows = query_record_model.searchQueryRecords(
        user_id=body.user_id,
        query_text=body.query_text,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=_as_public_records(rows),
    )


def filterQueryRecord(body: query_record_type.FilterQueryRecordBody) -> ApiResponse:
    query_types = [qt.value for qt in body.query_type] if body.query_type else None
    rows = query_record_model.filterQueryRecords(
        user_id=body.user_id or None,
        query_type=query_types,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=_as_public_records(rows),
    )


def updateQueryRecord(body: query_record_type.UpdateQueryRecordBody) -> ApiResponse:
    existing = query_record_model.getQueryRecordByID(body.id)
    if existing is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Query record not found",
            data=None,
        )
    if (
        body.user_id is None
        and body.query_type is None
        and body.query_text is None
        and body.answer is None
    ):
        return ApiResponse(
            success=True,
            code=status.HTTP_200_OK,
            message=None,
            data=_as_public_record(existing),
        )
    updated = query_record_model.updateQueryRecord(body)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=_as_public_record(updated),
    )


def removeQueryRecord(body: query_record_type.RemoveQueryRecordBody) -> ApiResponse:
    if query_record_model.getQueryRecordByID(body.id) is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Query record not found",
            data=None,
        )
    removed = query_record_model.removeQueryRecordByID(body.id)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=removed,
    )
