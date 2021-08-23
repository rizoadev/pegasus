# DB Mongo
#
# Python connect to mongodb as usual

import pymongo
from libs.logs import Exc, Log


class MongoConnect:
    def __init__(self, uri, db):
        self.uri = uri
        self.db = db

    async def connect(self):
        exc = Exc.create_exception()

        try:

            Log(f'engine start: konek ke mongo_db: {self.db}').send()

            # create connection to mongodb
            mongo = pymongo.MongoClient(self.uri)
            return mongo[self.db]
            '''with pymongo.MongoClient(self.uri) as client:
                mongo = client
                return mongo[self.db]'''

        except Exception as e:
            # send exception msg
            exc.exception(e)
            return None
