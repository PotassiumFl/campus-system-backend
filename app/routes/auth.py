from fastapi import APIRouter, HTTPException, status

from app.schemas.models import ApiResponse, LoginBody, RegisterBody
from db.user_repository import get_password, insert_user, user_exists

router = APIRouter()


@router.post("/register", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterBody) -> ApiResponse:
    if user_exists(body.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    hashed = hash(body.password)
    insert_user(body.name, hashed)

    return ApiResponse(
        success=True,
        code=status.HTTP_201_CREATED,
        message="Created",
        data={"name": body.name},
    )


@router.post("/login", response_model=ApiResponse, status_code=status.HTTP_200_OK)
async def login(body: LoginBody) -> ApiResponse:
    if not user_exists(body.name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    stored = get_password(body.name)
    if stored is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    hashed = hash(body.password)
    if hashed != stored:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password not correct",
        )

    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message="Logged in",
        data={"name": body.name},
    )

