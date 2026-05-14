from fastapi import APIRouter, status

from app.controllers import event as event_controller
from app.type import event as event_type
from app.type.response import ApiResponse

router = APIRouter()


@router.post("/upload", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def upload(body: event_type.UploadEventBody) -> ApiResponse:
    return event_controller.uploadEvent(body)


@router.post("/search", response_model=ApiResponse)
async def search(body: event_type.SearchEventBody) -> ApiResponse:
    return event_controller.searchEvent(body)


@router.post("/filter", response_model=ApiResponse)
async def filter_events(body: event_type.FilterEventBody) -> ApiResponse:
    return event_controller.filterEvent(body)


@router.post("/update", response_model=ApiResponse)
async def update(body: event_type.UpdateEventBody) -> ApiResponse:
    return event_controller.updateEvent(body)


@router.post("/remove", response_model=ApiResponse)
async def remove(body: event_type.RemoveEventBody) -> ApiResponse:
    return event_controller.removeEvent(body)
