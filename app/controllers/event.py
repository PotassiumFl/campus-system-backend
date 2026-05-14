from starlette import status

import app.model.building as building
import app.model.event as event
import app.type.event as event_type
from app.type.response import ApiResponse


def uploadEvent(body: event_type.UploadEventBody) -> ApiResponse:
    row = building.getBuildingByName(body.building_name)
    if row is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Building not found",
            data=None,
        )
    created = event.createEvent(
        event_type.CreateEventBody(
            building_id=row["building_id"],
            event_name=body.event_name,
            start_time=body.start_time,
            end_time=body.end_time,
            organizer=body.organizer,
            description=body.description,
        )
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_201_CREATED,
        message=None,
        data=created,
    )


def searchEvent(body: event_type.SearchEventBody) -> ApiResponse:
    rows = event.searchEvents(
        building_name=body.building_name,
        event_name=body.event_name,
        organizer=body.organizer,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=rows,
    )


def filterEvent(body: event_type.FilterEventBody) -> ApiResponse:
    rows = event.filterEvents(
        building_name=body.building_name,
        event_name=body.event_name,
        organizer=body.organizer,
        start_time=body.start_time,
        end_time=body.end_time,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=rows,
    )


def updateEvent(body: event_type.UpdateEventBody) -> ApiResponse:
    existing = event.getEventByID(body.event_id)
    if existing is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Event not found",
            data=None,
        )
    if body.building_id is not None:
        b = building.getBuildingByID(body.building_id)
        if b is None:
            return ApiResponse(
                success=False,
                code=status.HTTP_404_NOT_FOUND,
                message="Building not found",
                data=None,
            )
    if (
        body.building_id is None
        and body.event_name is None
        and body.start_time is None
        and body.end_time is None
        and body.organizer is None
        and body.description is None
    ):
        return ApiResponse(
            success=True,
            code=status.HTTP_200_OK,
            message=None,
            data=existing,
        )
    updated = event.updateEvent(body)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=updated,
    )


def removeEvent(body: event_type.RemoveEventBody) -> ApiResponse:
    if event.getEventByID(body.event_id) is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Event not found",
            data=None,
        )
    removed = event.removeEventByID(body.event_id)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=removed,
    )
