from fastapi import FastAPI, APIRouter
from ..routes import signup


def setup_routes(app: FastAPI):
    router = APIRouter()
    router.include_router(signup.router, prefix="/signup")
    app.include_router(router, prefix="/api")
