"""Router layer: URL wiring per domain — mount prefixes here (like a routers index)."""

from fastapi import FastAPI

from app.routers import building
from app.routers import campus
from app.routers import facility


def register_routers(app: FastAPI) -> None:
    app.include_router(campus.router, prefix="/campus", tags=["campus"])
    app.include_router(building.router, prefix="/building", tags=["building"])
    app.include_router(facility.router, prefix="/facility", tags=["facility"])
