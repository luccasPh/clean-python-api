from fastapi import APIRouter, Request, Response

from ..adapters.fastapi_route_adapter import adpter_route
from ..factories.signup.signup_factory import make_signup_controller

router = APIRouter()


@router.post("")
async def create_account(request: Request, response: Response):
    return await adpter_route(request, response, make_signup_controller())
