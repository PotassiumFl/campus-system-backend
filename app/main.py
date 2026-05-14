from fastapi import FastAPI

from app.exception_handlers import register_exception_handlers
from app.routers import register_routers


def create_app() -> FastAPI:
    app = FastAPI(title="DBDesignPy API", version="1.0.0")
    register_exception_handlers(app)
    register_routers(app)
    return app


app = create_app()

