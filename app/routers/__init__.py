"""Router layer: URL wiring per domain — mount prefixes here (like a routers index)."""

from fastapi import FastAPI

from app.routers import campus


def register_routers(app: FastAPI) -> None:
    app.include_router(campus.router, prefix="/campus", tags=["campus"])
