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
