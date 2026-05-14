import hashlib
import hmac
import secrets
from typing import Any

from starlette import status

import app.model.user_account as user_account_model
import app.type.userAccount as user_account_type
from app.type.response import ApiResponse

_PBKDF2_ITERATIONS = 390_000


def _hash_password(plain: str) -> str:
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        plain.encode("utf-8"),
        salt,
        _PBKDF2_ITERATIONS,
    )
    return f"pbkdf2_sha256${_PBKDF2_ITERATIONS}${salt.hex()}${dk.hex()}"


def _verify_password(plain: str, stored: str) -> bool:
    try:
        parts = stored.split("$")
        if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
            return False
        iterations = int(parts[1])
        salt = bytes.fromhex(parts[2])
        expected = bytes.fromhex(parts[3])
    except (ValueError, TypeError):
        return False
    actual = hashlib.pbkdf2_hmac(
        "sha256",
        plain.encode("utf-8"),
        salt,
        iterations,
    )
    return hmac.compare_digest(actual, expected)


def _as_public_user(row: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in row.items() if k != "password"}


def register(body: user_account_type.AuthRegisterBody) -> ApiResponse:
    if user_account_model.getUserAccountByUsername(body.username) is not None:
        return ApiResponse(
            success=False,
            code=status.HTTP_409_CONFLICT,
            message="Username already exists",
            data=None,
        )
    hashed = _hash_password(body.password)
    created = user_account_model.createUserAccount(
        user_account_type.CreateUserAccountBody(
            username=body.username,
            password=hashed,
            user_role=user_account_type.UserRole.user,
        )
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_201_CREATED,
        message=None,
        data=_as_public_user(created) if created else None,
    )


def updateAccount(body: user_account_type.AuthUpdateBody) -> ApiResponse:
    row = user_account_model.getUserAccountByID(body.user_id)
    if row is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="User not found",
            data=None,
        )
    if (
        body.username is None
        and body.password is None
        and body.user_role is None
    ):
        return ApiResponse(
            success=True,
            code=status.HTTP_200_OK,
            message=None,
            data=_as_public_user(row),
        )
    if body.username is not None:
        other = user_account_model.getUserAccountByUsername(body.username)
        if other is not None and other["user_id"] != body.user_id:
            return ApiResponse(
                success=False,
                code=status.HTTP_409_CONFLICT,
                message="Username already exists",
                data=None,
            )
    if body.password is not None and _verify_password(
        body.password, row["password"]
    ):
        return ApiResponse(
            success=False,
            code=status.HTTP_400_BAD_REQUEST,
            message="New password must differ from the current password",
            data=None,
        )
    hashed = (
        _hash_password(body.password) if body.password is not None else None
    )
    updated = user_account_model.updateUserAccount(
        user_account_type.UpdateUserAccountBody(
            user_id=body.user_id,
            username=body.username,
            password=hashed,
            user_role=body.user_role,
        )
    )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=_as_public_user(updated) if updated else None,
    )


def login(body: user_account_type.AuthLoginBody) -> ApiResponse:
    row = user_account_model.getUserAccountByUsername(body.username)
    if row is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="User not found",
            data=None,
        )
    stored = row["password"]
    if not _verify_password(body.password, stored):
        return ApiResponse(
            success=False,
            code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid password",
            data=None,
        )
    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=_as_public_user(row),
    )
