# JWT auth token
#
# Copyright (c) Riza Masykur 2021.
#
# History:
# 0.1   17-08-21 yk     Created

import jwt
import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta
from libs.logs import Log


class Auth():
    security = HTTPBearer()
    secret = os.getenv('SECRET') or 'RIZASCT'

    def check(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def encode_token(self, user_id):
        payload = {
            # 'exp': datetime.utcnow() + timedelta(days=360, minutes=5),
            'exp': datetime.utcnow() + timedelta(days=360, minutes=1),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            sub = payload.get('sub')

            # writing logline
            Log(f'token valid: {sub}').send()

            return sub
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Login expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')
