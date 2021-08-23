from hashlib import blake2b
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, validator
from libs.auth.password import Password


class UserEmail(BaseModel):
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserRekening(BaseModel):
    bank: Optional[str] = ''
    cabang: Optional[str] = ''
    norek: Optional[str] = ''
    nama: Optional[str] = ''


class UserAddress(BaseModel):
    nama: Optional[str] = ''
    whatsapp: Optional[str] = ''
    provinsi: Optional[int] = 0
    provinsi_name: Optional[str] = ''
    kabupaten: Optional[int] = 0
    kabupaten_name: Optional[str] = ''
    kecamatan: Optional[int] = 0
    kecamatan_name: Optional[str] = ''
    kelurahan: Optional[int] = 0
    kelurahan_name: Optional[str] = ''
    kodepos: Optional[str] = ''
    alamat: Optional[str] = ''


class UserMarketplace(BaseModel):
    instagram: Optional[str] = ''
    shopee: Optional[str] = ''
    tokopedia: Optional[str] = ''
    bukalapak: Optional[str] = ''
    lazada: Optional[str] = ''
    lainnya: Optional[str] = ''


class UserBase(BaseModel):
    fullname: str
    email: str
    org: Optional[str] = ''
    orgs: Optional[list] = []
    avatar: Optional[str] = ''
    status: Optional[str] = 'inactive'
    role: str = 'agen'
    meta: Optional[dict] = {}
    verified: Optional[bool] = False
    role: Optional[str] = ''
    created: datetime = datetime.now()
    modified: datetime = datetime.now()
    created_date: datetime = None
    active_date: datetime = None
    wallet_balance: int = 0
    referral: Optional[str] = ''
    badges: Optional[list] = []
    libur: Optional[bool] = False
    whatsapp: Optional[str] = ''
    whatsapp_text: Optional[str] = ''
    rekening: Optional[UserRekening] = UserRekening()
    online_store: Optional[UserMarketplace] = UserMarketplace()
    alamat_landing: Optional[UserAddress] = UserAddress()
    alamat_pengiriman: Optional[UserAddress] = UserAddress()

    # validation at field level
    @validator("whatsapp")
    def phone_length(cls, v):
        if len(str(v)) < 10:
            raise ValueError("Phone number must be of ten digits")
        return v


class UserToken(BaseModel):
    login_status: Optional[str] = 'success'
    token: Optional[str] = None


class UserBasePassword(UserBase):
    password: str

    @validator('password', always=True)
    def set_pass(cls, v):
        t = Password().get_password_hash(v)
        return t


class UserRegister(UserBasePassword):
    uid: str = None

    @validator('uid', always=True)
    def set_id(cls, v, values):
        m = values['email']
        h = blake2b(digest_size=4)
        h.update(m.encode('utf-8'))
        t = h.hexdigest()
        return f'u{str(t)}'


class UserNewRegisterRes(BaseModel):
    fullname: str
    email: str
    whatsapp: str


class UserNewRegister(BaseModel):
    fullname: str
    password: str
    email: str
    whatsapp: str


class UserChangePass(BaseModel):
    oldpassword: str
    newpassword: str


class UserCekPassword(BaseModel):
    password: str


class UserUpdate(BaseModel):
    update: dict