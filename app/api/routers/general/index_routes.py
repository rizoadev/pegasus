#===========================================
# homepage routes
#===========================================
from fastapi import APIRouter, Request

route = APIRouter()


@route.get("/")
async def indexpage(request: Request):
    return {'status': 'ok'}


@route.get("/s")
async def indexpage(request: Request):
    return {
        'status': request.app.state.author,
        'org': request.app.state.config['main']['org']
    }
