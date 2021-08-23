import string
import random
from datetime import datetime
from fastapi import Request
from libs.monga import Monga
from libs.logs import Exc
from libs.auth.password import Password
from api.schemas.users import UserLogin, UserNewRegister, UserEmail, UserRegister

exc = Exc.create_exception()
collection = 'main_accounts'


class Users:
    def find_me(user: UserLogin, request: Request):
        '''
        find userdata by email or whatsapp or _id
        '''
        m = Monga(request.app.state.mongo[collection])

        # try 3 options
        s = m.find_one({'email': user.email})
        if not s:
            m.find_one({'whatsapp': user.email})
        if not s:
            m.find_one({'_id': user.email})

        # with http exception
        if s:
            return s
        else:
            return None

    def find_me_by_id(userid: str, request: Request):
        '''
        find userdata by _id
        '''
        s = Monga(request.app.state.mongo[collection]).find_one(
            {'_id': userid})
        # with http exception
        if s:
            return s
        else:
            return None

    def find_me_by_email(data: UserEmail, request: Request):
        s = Monga(request.app.state.mongo[collection]).find_one(
            {'email': data.email})
        return s

    def find_my_reset_code(code: str, request: Request):
        '''
        find meta.forgot_password by _id
        '''
        s = Monga(request.app.state.mongo[collection]).find_one(
            {'meta.forgot_password': code})
        # with http exception
        if s:
            return s
        else:
            return None

    def register(user: UserNewRegister, request: Request):
        newuser = UserRegister(**user.dict())
        try:
            user_reg = Monga(
                request.app.state.mongo[collection]).insert_one(newuser)
            if user_reg:
                return newuser
            else:
                return None

        except Exception as e:
            exc.exception(e)
            return None

    def update_me(userid: str, update: dict, request: Request):
        '''
        update data by _id
        '''

        new_update = update.dict()['update']

        if 'password' in new_update:
            del new_update['password']

        if '_id' in new_update:
            del new_update['_id']

        # update db
        s = Monga(request.app.state.mongo[collection]).find_one_and_update(
            {'_id': userid}, {'$set': new_update})
        if s:
            return s
        else:
            return None

    def change_password(userid: str, newpassword: str, request: Request):
        '''
        change password by userid
        '''
        new_pass_hash = Password().get_password_hash(newpassword)

        # change db
        s = Monga(request.app.state.mongo[collection]).find_one_and_update(
            {'_id': userid}, {
                '$set': {
                    'password': new_pass_hash,
                    'modified': datetime.now(),
                    '_last_change_msg': 'change password'
                },
                '$unset': {
                    'meta.forgot_password': 0
                }
            })
        # with http exception
        if s:
            return s
        else:
            return None

    def generate_reset_code(data: UserEmail, request: Request):
        '''
        add unique code to user db
        '''
        m = Monga(request.app.state.mongo[collection])
        rdt = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=20))

        # update db
        upd = m.find_one_and_update({'email': data['email']},
                                    {'$set': {
                                        'meta.forgot_password': rdt
                                    }})
        return True