from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .routes import setup_routes
from .openapi import setup_openapi
from ..middlewares.route_middleware import route_middleware

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
    return await route_middleware(request, call_next)


setup_routes(app)

setup_openapi(app)
