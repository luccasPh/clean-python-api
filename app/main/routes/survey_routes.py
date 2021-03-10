from fastapi import APIRouter, Request, Response

from ..adapters.fastapi_route_adapter import adpter_route
from ..factories.add_survey.add_survey_factory import make_add_survey_controller
from ..factories.load_surveys.load_surveys_factory import make_load_surveys_controller

router = APIRouter()


@router.post("/surveys")
async def add_surveys(request: Request, response: Response):
    return await adpter_route(request, response, make_add_survey_controller())


@router.get("/surveys")
async def load_surveys(request: Request, response: Response):
    return await adpter_route(request, response, make_load_surveys_controller())
