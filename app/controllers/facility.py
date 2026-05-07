from starlette import status

import app.model.building as building
import app.model.facility as facility
import app.type.facility as facilityType
from app.type.response import ApiResponse


def uploadFacility(body: facilityType.UploadFacilityBody) -> ApiResponse:
    row = building.getBuildingByName(body.building_name)
    if row is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="Building not found",
            data=None,
        )
    created = facility.createFacility(
        facilityType.CreateFacilityBody(
            building_id=row["building_id"],
            name=body.facility_name,
            type=body.facility_type,
            openTime=body.openTime,
        )
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_201_CREATED,
        message=None,
        data=created,
    )
