from starlette import status

import app.model.campus as campus
import app.type.campus as cpType
from app.type.response import ApiResponse


def uploadCampus(body: list[cpType.CreateCampusBody]) -> ApiResponse:
    created = [campus.createCampus(item) for item in body]
    return ApiResponse(
        success=True,
        code=status.HTTP_201_CREATED,
        message=None,
        data=created,
    )
