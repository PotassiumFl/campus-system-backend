from starlette import status

import app.model.building as building
import app.model.campus as campus
import app.type.building as buildingType
from app.type.response import ApiResponse


def uploadBuilding(body: buildingType.UploadBuildingBody) -> ApiResponse:
    row = campus.getCampusByName(body.campus_name)
    if row is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Campus not found",
            data=None,
        )
    created = building.createBuilding(
        buildingType.CreateBuildingBody(
            building_name=body.building_name,
            campus_id=row["campus_id"],
            building_type=body.building_type,
        )
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_201_CREATED,
        message=None,
        data=created,
    )


def searchBuilding(body: buildingType.SearchBuildingBody) -> ApiResponse:
    rows = building.searchBuildings(
        campus_name=body.campus_name,
        building_name=body.building_name,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=rows,
    )


def filterBuilding(body: buildingType.FilterBuildingBody) -> ApiResponse:
    rows = building.filterBuildings(
        campus_name=body.campus_name,
        building_name=body.building_name,
        building_type=body.building_type,
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=rows,
    )


def updateBuilding(body: buildingType.UpdateBuildingBody) -> ApiResponse:
    existing = building.getBuildingByID(body.building_id)
    if existing is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Building not found",
            data=None,
        )
    if body.campus_id is not None:
        c = campus.getCampusByID(body.campus_id)
        if c is None:
            return ApiResponse(
                success=False,
                code=status.HTTP_404_NOT_FOUND,
                message="Campus not found",
                data=None,
            )
    if body.building_name is None and body.campus_id is None and body.building_type is None:
        return ApiResponse(
            success=True,
            code=status.HTTP_200_OK,
            message=None,
            data=existing,
        )
    updated = building.updateBuilding(body)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=updated,
    )


def removeBuilding(body: buildingType.RemoveBuildingBody) -> ApiResponse:
    if building.getBuildingByID(body.building_id) is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Building not found",
            data=None,
        )
    removed = building.removeBuildingByID(body.building_id)
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=removed,
    )
