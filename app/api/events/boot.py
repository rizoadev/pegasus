# Startup Script
#
# Autorun this class on startup
#
# Copyright (c) Riza Masykur 2021.
#
# History:
# 0.1   17-08-21 yk     Created

import os
from fastapi import FastAPI
from api.events.config import Config
from api.core.db.db_mongo import MongoConnect
from libs.pubsub import PubSub


class Boot:
    def booting(app: FastAPI):
        def load():
            return Config.load()

        async def connect_mongo_1(conf):
            return await MongoConnect(conf['main']['mongodb'],
                                      conf['main']['mongodb_db']).connect()

        async def connect_mongo_logs(conf):
            return await MongoConnect(conf['logs']['mongodb'],
                                      conf['logs']['mongodb_db']).connect()

        # Load config & Databases
        async def start_app() -> None:
            conf = load()

            # add to environ
            os.environ['SECRET'] = conf['security']['secret']

            app.state.config = conf
            app.state.author = 'riza masykur'
            app.state.mongo = await connect_mongo_1(conf)
            app.state.mongo_log = await connect_mongo_logs(conf)
            app.state.pubsub = PubSub(conf['gcp_pubsub'])

        return start_app
