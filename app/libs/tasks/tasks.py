from fastapi import Request
from dataclasses import dataclass
from .task_sendlog import TaskSendlog

pubsub_topic = 'test001'


@dataclass
class Tasks:
    namespace: str
    name: str
    msg: str
    data: dict

    def send(self, request: Request):

        pubsub = request.app.state.pubsub
        publisher = pubsub.pub()

        # send msg to pubsub
        pid = pubsub.send(
            publisher, {
                'topic': pubsub_topic,
                'namespace': self.namespace,
                'subname': self.name,
                'delay': 0,
                'data': self.data.dict()
            })

        TaskSendlog(org=request.app.state.config['main']['org'],
                    namespace=self.namespace,
                    subname=self.name,
                    msg=self.msg,
                    data=self.data,
                    msg_id=int(pid)).send(request.app.state.mongo_log)

        print('==================================')
        print(
            f'\33[32mSend Task: {self.namespace} --> {self.name} --> ID:{pid}',
            '\033[0m')
        print('==================================')
