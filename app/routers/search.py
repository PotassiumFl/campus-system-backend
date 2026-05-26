from fastapi import APIRouter

from app.controllers import search as search_controller
from app.type import search as search_type
from app.type.response import ApiResponse

router = APIRouter()


@router.post("/search", response_model=ApiResponse)
async def search(body: search_type.NaturalSearchBody) -> ApiResponse:
    return search_controller.naturalLanguageSearch(body)
