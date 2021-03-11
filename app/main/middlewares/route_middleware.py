from fastapi import Request

from ..adapters.fastapi_middleware_adapter import adpter_middleware
from ..factories.middlewares.aut_middleware_factory import make_auth_middleware


async def route_middleware(request: Request, call_next):
    if request.url.path == "/api/surveys":
        if request.method == "POST":
            aut_middleware = make_auth_middleware("admin")
        else:
            aut_middleware = make_auth_middleware()
        return await adpter_middleware(request, call_next, aut_middleware)
    elif request.url.path.split("/")[-1] == "results":
        return await adpter_middleware(request, call_next, make_auth_middleware())
    else:
        return await call_next(request)
