from fastapi import APIRouter, Request, Response

from ..adapters.fastapi_route_adapter import adpter_route
from ..factories.survey.add_survey_factory import make_add_survey_controller

router = APIRouter()


@router.post("/surveys")
async def create_survey(request: Request, response: Response):
    return await adpter_route(request, response, make_add_survey_controller())
