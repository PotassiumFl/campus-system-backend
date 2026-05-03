from typing import Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool
    code: int
    message: str | None
    data: Any | None = None
