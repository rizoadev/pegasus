import os
#===========================================
# global sandbox
#===========================================
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from api.schemas.users import UserBase, UserLists
from libs.monga import Monga
from libs.auth import Auth

route = APIRouter()
auth = Auth()


def FCall(request: Request):
    """konek langsung ke collection"""
    return Monga(request.app.state.mongo.m_users)


@route.get("/")
async def index(request: Request):
    #r = Monga(request.app.state.mongo.m_users).find_one({})
    #return {'t': r}
    return {'secret': os.environ['SECRET']}


@route.get("/token")
async def gettoken():
    h = auth.encode_token('me')
    return HTMLResponse(content=h, status_code=200)


@route.get("/auth")
async def authd(request: Request):
    return {'secret': os.environ['SECRET']}


@route.get("/lists")
async def lists(m=Depends(FCall)):
    getall = m.aggregate([])
    count = m.count({})

    res = UserLists(results=getall).dict()
    res.update({'count': count})
    return res


@route.get("/insert")
async def insert(m=Depends(FCall)):
    # define user data1
    ts = UserBase(
        fullname='nicole admin',
        password='pass124',
        email='nicole@gmail.com',
        role="agen",
        whatsapp="+68254545155",
    )

    # insert to DB
    insx = m.insert_one(ts)
    if insx:
        return {'status': insx, 's': ts}
    else:
        return {'status': False, 's': ts}
