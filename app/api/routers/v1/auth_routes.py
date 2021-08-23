from fastapi import APIRouter, Depends, HTTPException, Request
from libs.auth import Auth
from libs.auth.password import Password
from libs.tasks import Tasks
from api.models.users import Users
from api.schemas.users import UserBase, UserLogin, UserCekPassword, UserToken, UserEmail, UserNewRegister, UserChangePass, UserUpdate, UserNewRegisterRes

route = APIRouter()
auth = Auth()


@route.post("/register", summary="Register", response_model=UserNewRegisterRes)
async def auth_register(request: Request,
                        user: UserNewRegister = Depends(Users.register)):

    if not user:
        raise HTTPException(status_code=400, detail='register failed')
    else:

        # send task queue
        Tasks(namespace='auth',
              name='auth_register',
              msg='register user baru',
              data=user).send(request)

        return user


@route.post("/login", response_model=UserToken)
async def auth_login(request: Request,
                     user: UserLogin = Depends(Users.find_me)):

    # after query
    if 'password' in user:
        bodi = await request.json()
        plainp = bodi['password']
        cekpass = Password().verify_password(plainp, user['password'])

        if cekpass:
            # return with bearer token
            user.update({'token': auth.encode_token(user['_id'])})

            # send task queue
            print('login', user['fullname'])
            '''fullname = user['fullname']
            Tasks(namespace='auth',
                  name='auth_login',
                  msg=f"login to app: {fullname}",
                  data=user).send(request)'''

            return user

        else:
            raise HTTPException(status_code=400, detail='login failed')
    else:
        raise HTTPException(status_code=400, detail='wrong email or password')


@route.get("/me",
           summary="My profile data",
           dependencies=[Depends(auth.check)],
           response_model=UserBase)
async def auth_me(request: Request, userid: str = Depends(auth.check)):
    s = Users.find_me_by_id(userid, request)
    if not s:
        raise HTTPException(status_code=400, detail='forbidden')
    else:
        return s


@route.post("/check_available_email", summary="Check email waktu pendaftaran")
async def auth_checkmail(data: UserEmail = Depends(Users.find_me_by_email)):
    if data:
        raise HTTPException(status_code=400, detail='email exists')
    return {'detail': 'email available'}


@route.post("/forgot_password", summary="Request password reset")
async def auth_forgot_password(request: Request,
                               data: UserEmail = Depends(
                                   Users.find_me_by_email)):
    if data:

        # generate unique reset code
        Users.generate_reset_code(data, request)

        # send task queue
        Tasks(namespace='auth',
              name='forgot_password',
              msg='mengirim email',
              data=data).send()

        return {'detail': 'email sent'}
    else:
        raise HTTPException(status_code=400, detail='email not found')


@route.post("/reset_password/{code}", summary="Reset password with code")
async def auth_reset_password(request: Request, data: UserCekPassword, code):

    s = Users.find_my_reset_code(code, request)
    if not s:
        raise HTTPException(status_code=400, detail='wrong reset code')
    else:

        # after query
        if 'password' in s:

            # cek code
            if code == s['meta']['forgot_password']:

                # change password
                Users.change_password(s['_id'], data.password, request)

                # send task
                Tasks(namespace='auth',
                      name='change_password',
                      msg='ganti password success',
                      data={
                          'userid': s['_id']
                      }).send()

                return {
                    'status': True,
                    'detail': 'password changed succesfully'
                }
            else:
                raise HTTPException(status_code=400,
                                    detail='change password failed')
        else:
            raise HTTPException(status_code=400, detail='wrong password')


@route.post("/check_password", summary="Validate password")
async def auth_checkpass(request: Request,
                         data: UserCekPassword,
                         userid: str = Depends(auth.check)):
    s = Users.find_me_by_id(userid, request)

    # after query
    if 'password' in s:
        cekpass = Password().verify_password(data.password, s['password'])
        if cekpass:
            return {'password': True}

        else:
            raise HTTPException(status_code=400, detail='wrong password')
    else:
        raise HTTPException(status_code=400, detail='wrong password')


@route.post("/change_password", summary="Change password from Dashboard")
async def auth_changepassword(
        request: Request,
        data: UserChangePass,
        userid: str = Depends(auth.check),
):

    s = Users.find_me_by_id(userid, request)
    # after query
    if 'password' in s:

        # validate pass
        cekpass = Password().verify_password(data.oldpassword, s['password'])
        if cekpass:

            # change password
            Users.change_password(userid, data.newpassword, request)

            # send task
            Tasks(namespace='auth',
                  name='change_password',
                  msg='ganti password success',
                  data={
                      'userid': userid
                  }).send()

            return {'status': True, 'detail': 'password changed succesfully'}
        else:
            raise HTTPException(status_code=400, detail='wrong password')
    else:
        raise HTTPException(status_code=400, detail='wrong password')


@route.post("/update", summary="Update my Data")
async def auth_update_me(request: Request,
                         data: UserUpdate,
                         userid: str = Depends(auth.check)):
    s = Users.update_me(userid, data, request)
    if not s:
        raise HTTPException(status_code=400, detail='update failed')
    else:

        # send task
        Tasks(namespace='auth',
              name='update',
              msg='update profile success',
              data={
                  'userid': userid,
                  'update': data.dict()['update']
              }).send()

        return {'update': 'success'}
