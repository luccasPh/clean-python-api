from fastapi import APIRouter, Request, Response

from ..adapters.fastapi_route_adapter import adpter_route
from ..factories.save_survey_result.save_survey_result_factory import (
    make_save_survey_result_controller,
)


router = APIRouter()


@router.post("/surveys/{survey_id}/results")
async def add_surveys(request: Request, response: Response):
    return await adpter_route(request, response, make_save_survey_result_controller())
