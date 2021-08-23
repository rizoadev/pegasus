'''
send task data to mongo
'''
from pydantic import BaseModel
from dataclasses import dataclass
from datetime import datetime
from libs.monga import Monga

collection = 'backend_logs'


class TSData(BaseModel):
    org: str
    namespace: str
    subname: str
    msg: str
    created: datetime
    status: str
    content: dict
    msg_id: int


@dataclass
class TaskSendlog:
    org: str
    namespace: str
    subname: str
    msg: str
    data: dict
    msg_id: int

    def send(self, mongo_log):
        crtd = datetime.now()
        ndata = TSData(org=self.org,
                       namespace=self.namespace,
                       subname=self.subname,
                       msg=self.msg,
                       created=crtd,
                       content=self.data.dict(),
                       status='pending',
                       msg_id=self.msg_id)

        Monga(mongo_log[collection]).insert_one(ndata)
