from fastapi import APIRouter
from app.api.routes import evaluations, status

api_router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)

api_router.include_router(evaluations.router)
api_router.include_router(status.router)
