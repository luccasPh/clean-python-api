from fastapi import FastAPI, APIRouter
from ..routes import auth_routes as auth
from ..routes import survey_routes as survey
from ..routes import survey_result_routes as survey_result


def setup_routes(app: FastAPI):
    router = APIRouter()
    router.include_router(auth.router)
    router.include_router(survey.router)
    router.include_router(survey_result.router)
    app.include_router(router, prefix="/api")
