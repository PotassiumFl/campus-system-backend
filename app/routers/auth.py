from fastapi import APIRouter, status

from app.controllers import auth as auth_controller
from app.type import userAccount as user_account_type
from app.type.response import ApiResponse

router = APIRouter()


@router.post("/register", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def register(body: user_account_type.AuthRegisterBody) -> ApiResponse:
    return auth_controller.register(body)


@router.post("/login", response_model=ApiResponse)
async def login(body: user_account_type.AuthLoginBody) -> ApiResponse:
    return auth_controller.login(body)


@router.post("/update", response_model=ApiResponse)
async def update(body: user_account_type.AuthUpdateBody) -> ApiResponse:
    return auth_controller.updateAccount(body)
