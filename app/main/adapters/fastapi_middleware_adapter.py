from fastapi import Request
from fastapi.responses import JSONResponse

from app.presentation import Middleware, HttpRequest


async def adpter_middleware(request: Request, call_next, middleware: Middleware):
    headers = request.headers
    http_response = middleware.handle(HttpRequest(headers=headers))
    if http_response.status_code == 200:
        request.state.account_id = http_response.body
        response = await call_next(request)
        return response
    else:
        return JSONResponse(
            status_code=http_response.status_code, content=http_response.body
        )
