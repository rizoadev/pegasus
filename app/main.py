from functools import lru_cache
from fastapi import FastAPI
from api.events.boot import Boot

from api.routers.general import route as routeAll
#from api.routers.sandbox import route as routeSandbox
from api.routers.v1 import route as routeV1

PROJECT_NAME = 'pegasus'
PROJECT_DESC = 'Fast & Clean'
DEBUG = False
VERSION = '1.0.0'


@lru_cache()
def get_settings():
    return {'small': 'inside'}


def init_app():
    app = FastAPI(title=PROJECT_NAME,
                  description=PROJECT_DESC,
                  debug=DEBUG,
                  version=VERSION)

    # engine start, connect db
    app.add_event_handler("startup", Boot.booting(app))

    # add routes
    app.include_router(routeV1)
    app.include_router(routeAll)
    #app.include_router(routeSandbox)

    return app


# run boss
app = init_app()