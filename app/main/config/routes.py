from fastapi import FastAPI, APIRouter
from ..routes import auth_route as auth


def setup_routes(app: FastAPI):
    router = APIRouter()
    router.include_router(auth.router)
    app.include_router(router, prefix="/api")
