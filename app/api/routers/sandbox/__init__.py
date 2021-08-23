from fastapi import APIRouter, Depends
from .sandbox import route as sandbox
from libs.auth import Auth

auth = Auth()

route = APIRouter(prefix="/sandbox")  # , dependencies=[Depends(auth.check)]
route.include_router(sandbox, tags=["Sandbox Routes"])

__all__ = ["route"]