import json

from fastapi import Request, Response

from app.presentation import Controller, HttpRequest


async def adpter_route(request: Request, response: Response, controller: Controller):
    body = await request.body()
    headers = request.headers
    params = request.path_params
    account_id = getattr(request.state, "account_id", None)
    http_response = controller.handle(
        HttpRequest(
            headers=headers,
            params=params,
            account_id=account_id,
            body=json.loads(body or "{}"),
        )
    )
    response.status_code = http_response.status_code
    if http_response.status_code == 204:
        return Response(status_code=204)
    return http_response.body
