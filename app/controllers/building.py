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
            name=body.building_name,
            campus_id=row["campus_id"],
            type=body.building_type,
        )
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_201_CREATED,
        message=None,
        data=created,
    )
