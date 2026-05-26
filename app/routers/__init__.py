"""Router layer: URL wiring per domain — mount prefixes here (like a routers index)."""

from fastapi import FastAPI

from app.routers import auth
from app.routers import building
from app.routers import campus
from app.routers import course
from app.routers import event
from app.routers import facility
from app.routers import query_record
from app.routers import search
from app.routers import teach
from app.routers import teacher


def register_routers(app: FastAPI) -> None:
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(campus.router, prefix="/campus", tags=["campus"])
    app.include_router(building.router, prefix="/building", tags=["building"])
    app.include_router(facility.router, prefix="/facility", tags=["facility"])
    app.include_router(course.router, prefix="/course", tags=["course"])
    app.include_router(event.router, prefix="/event", tags=["event"])
    app.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
    app.include_router(teach.router, prefix="/teach", tags=["teach"])
    app.include_router(query_record.router, prefix="/query_record", tags=["query_record"])
    app.include_router(search.router, tags=["search"])
