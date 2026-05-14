from starlette import status

import app.model.campus as campus
import app.type.campus as campusType
from app.type.response import ApiResponse


def uploadCampus(body: campusType.CreateCampusBody) -> ApiResponse:
    created = campus.createCampus(body)
    return ApiResponse(
        success = True,
        code = status.HTTP_201_CREATED,
        message = None,
        data = created,
    )


def searchCampus(body: campusType.SearchCampusBody) -> ApiResponse:
    rows = campus.searchCampus(
        campus_name=body.campus_name, campus_address=body.campus_address
    )
    return ApiResponse(
        success = True,
        code = status.HTTP_200_OK,
        message = None,
        data = rows,
    )


def filterCampus(body: campusType.FilterCampusBody) -> ApiResponse:
    rows = campus.filterCampus(
        campus_name=body.campus_name, campus_address=body.campus_address
    )
    return ApiResponse(
        success = True,
        code = status.HTTP_200_OK,
        message = None,
        data = rows,
    )


def updateCampus(body: campusType.UpdateCampusBody) -> ApiResponse:
    existing = campus.getCampusByID(body.campus_id)
    if existing is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Campus not found",
            data=None,
        )
    if body.campus_name is None and body.campus_address is None:
        return ApiResponse(
            success=True,
            code=status.HTTP_200_OK,
            message=None,
            data=existing,
        )
    updated = campus.updateCampus(body)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=updated,
    )


def removeCampus(body: campusType.RemoveCampusBody) -> ApiResponse:
    if campus.getCampusByID(body.campus_id) is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Campus not found",
            data=None,
        )
    removed = campus.removeCampusByID(body.campus_id)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=removed,
    )
