from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .routes import setup_routes
from ..adapters.fastapi_middleware_adapter import adpter_middleware
from ..factories.middlewares.aut_middleware_factory import AuthMiddleware

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
    if request.url.path == "/api/surveys" and request.method == "POST":
        admin_auth = AuthMiddleware("admin")
        return await adpter_middleware(request, call_next, admin_auth)
    else:
        return await call_next(request)


setup_routes(app)
