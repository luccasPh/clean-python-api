from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .routes import setup_routes
from ..adapters.fastapi_middleware_adapter import adpter_middleware
from ..factories.middlewares.aut_middleware_factory import make_auth_middleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def custom_middlewares(request: Request, call_next):
    if request.url.path == "/api/surveys":
        if request.method == "POST":
            aut_middleware = make_auth_middleware("admin")
        else:
            aut_middleware = make_auth_middleware()
        return await adpter_middleware(request, call_next, aut_middleware)
    else:
        return await call_next(request)


setup_routes(app)
