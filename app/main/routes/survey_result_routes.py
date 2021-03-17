from fastapi import APIRouter, Request, Response

from ..adapters.fastapi_route_adapter import adpter_route
from ..factories.save_survey_result.save_survey_result_factory import (
    make_save_survey_result_controller,
)
from ..factories.load_survey_result.load_survey_result_factory import (
    make_load_survey_result_controller,
)


router = APIRouter()


@router.put("/surveys/{survey_id}/results")
async def save_survey_result(request: Request, response: Response):
    return await adpter_route(request, response, make_save_survey_result_controller())


@router.get("/surveys/{survey_id}/results")
async def load_survey_result(request: Request, response: Response):
    return await adpter_route(request, response, make_load_survey_result_controller())
