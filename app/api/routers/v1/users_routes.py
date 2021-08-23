#===========================================
# users v1 routes
#===========================================
from fastapi import APIRouter

route = APIRouter()


@route.get("/")
async def user_index():
    return {'status': 'ok'}


@route.get("/id/{userid}")
async def user_by_id():
    return {'status': 'ok'}


@route.post("/update/{userid}")
async def user_update():
    return {'status': 'ok'}


@route.post("/change_password/{userid}")
async def user_password_change():
    return {'status': 'ok'}


@route.delete("/delete/{userid}", summary='Delete User by UserID')
async def user_delete():
    return {'status': 'ok'}
