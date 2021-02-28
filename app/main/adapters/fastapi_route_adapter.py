from fastapi import Request, Response

from app.presentation import Controller, HttpRequest


async def adpter_route(request: Request, response: Response, controller: Controller):
    body = await request.json()
    http_response = controller.handle(HttpRequest(body))
    response.status_code = http_response.status_code
    return http_response.body
