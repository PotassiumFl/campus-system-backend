from fastapi import FastAPI

from app.exception_handlers import register_exception_handlers
from app.routes.auth import router as auth_router
from app.routes.course import router as course_router


def create_app() -> FastAPI:
    app = FastAPI()
    register_exception_handlers(app)
    app.include_router(auth_router)
    app.include_router(course_router)
    return app


app = create_app()

