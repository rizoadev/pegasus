from fastapi import APIRouter
from .auth_routes import route as auth_routes
#from .users_routes import route as users_routes

route = APIRouter(prefix="/v1")
route.include_router(auth_routes, tags=["v1 Auth"], prefix="/auth")
#route.include_router(users_routes, tags=["v1 Users"], prefix="/users")

__all__ = ["route"]