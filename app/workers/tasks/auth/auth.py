from workers.task_decorator import regtask


class Auth:
    @regtask
    def auth_register(config: dict, mongolog, namespace: str, subname: str,
                      msg_id: str, data: dict):
        print('nganu register')
        return True

    @regtask
    def auth_login(config: dict, mongolog, namespace: str, subname: str,
                   msg_id: str, data: dict):
        print('nganu login')
        return True