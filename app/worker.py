import asyncio
from libs.logs import Log
from api.events.config import Config
from workers.init_pubsub import Bot

config = Config.load()


async def init_worker(config):
    while True:

        await Bot(config).run()
        await asyncio.sleep(3)


if __name__ == '__main__':

    Log('worker start').send()

    loop = asyncio.new_event_loop()
    try:
        loop.create_task(init_worker(config))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
    finally:
        loop.close()
