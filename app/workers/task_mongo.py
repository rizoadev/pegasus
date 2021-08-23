from api.core.db.db_mongo import MongoConnect


async def connect_mongo_log(conf):
    return await MongoConnect(conf['logs']['mongodb'],
                              conf['logs']['mongodb_db']).connect()
