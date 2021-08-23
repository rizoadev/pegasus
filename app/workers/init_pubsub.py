import json
import asyncio
from pydantic import BaseModel, validator
from dataclasses import dataclass
from libs.pubsub import PubSub
from .task_job import Jobs
from .task_mongo import connect_mongo_log


class Msg(BaseModel):
    namespace: str
    subname: str
    delay: int
    message_id: str
    attributes: dict
    data: str

    # validation at field level
    @validator("data")
    def decodex(cls, v):
        return json.loads(v)


@dataclass
class Bot:
    config: dict
    subname = 'test001-sub'

    async def executor(self, mongolog, msg: Msg):
        '''dat = Msg(namespace=msg.attributes['namespace'],
                  subname=msg.attributes['subname'],
                  delay=int(msg.attributes['delay']),
                  publishtime=msg.publish_time,
                  attributes=msg.attributes,
                  message_id=msg.message_id,
                  data=msg.data.decode('utf-8'))'''

        # run task
        job = Jobs(config=self.config,
                   message_id=msg.message_id,
                   namespace=msg.attributes['namespace'],
                   subname=msg.attributes['subname'],
                   delay=int(msg.attributes['delay']),
                   data=msg.data.decode('utf-8'))

        await job.job(mongolog)

    async def run(self):
        gcp_config = self.config['gcp_pubsub']
        pubsub = PubSub(gcp_config)
        mongolog = await connect_mongo_log(self.config)
        while True:
            subscrb = pubsub.sub()
            with subscrb:
                subpath = subscrb.subscription_path(gcp_config["project_id"],
                                                    self.subname)

                # get messages
                response = subscrb.pull(request={
                    'subscription': subpath,
                    'max_messages': 3
                })

                ack_ids = []
                for msg in response.received_messages:

                    # print("Received: {}".format(msg.message))
                    await self.executor(mongolog, msg.message)

                    ack_ids.append(msg.ack_id)

                # Acknowledges the received messages so they will not be sent again.
                tot = len(response.received_messages)
                if tot > 0:
                    subscrb.acknowledge(request={
                        "subscription": subpath,
                        "ack_ids": ack_ids,
                    })

            await asyncio.sleep(2)
