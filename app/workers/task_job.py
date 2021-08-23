from dataclasses import dataclass
from workers.tasks.auth import Auth as auth


@dataclass
class Jobs:
    config: dict
    message_id: str
    namespace: str
    subname: str
    delay: int
    data: dict

    async def job(self, mongolog):

        # calling class auth
        if self.namespace == 'auth':
            c = getattr(auth, self.subname)
            c(self.config, mongolog, self.namespace, self.subname,
              self.message_id, self.data)
