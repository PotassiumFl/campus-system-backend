from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.models import ApiResponse


def _http_detail_message(detail: str | dict | list) -> str:
    if isinstance(detail, str):
        return detail
    return str(detail)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        payload: Any = ApiResponse(
            success=False,
            code=exc.status_code,
            message=_http_detail_message(exc.detail),
            data=None,
        ).model_dump()

        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        payload: Any = ApiResponse(
            success=False,
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Request validation failed",
            data=exc.errors(),
        ).model_dump()

        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=payload)

