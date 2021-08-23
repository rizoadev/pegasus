from datetime import datetime


def task_update_status(mongolog, id):
    mongolog.backend_logs.find_one_and_update(
        {'msg_id': id},
        {'$set': {
            'status': 'done',
            'completed': datetime.now()
        }})
    pass


def regtask(func):
    def inner(*args, **kwargs):
        print('==================================')
        print("\33[31mExecute job: ",
              f'{args[2]} --> {args[3]} --> ID:{args[4]}', "\033[0m")
        print('==================================')

        # update status
        c = func(*args, **kwargs)
        task_update_status(args[1], args[4])

        print('huasile', c)

    return inner
