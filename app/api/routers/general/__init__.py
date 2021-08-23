from fastapi import APIRouter
from .index_routes import route as index_routes

route = APIRouter()
route.include_router(index_routes, tags=["Homepage"])

__all__ = ["route"]