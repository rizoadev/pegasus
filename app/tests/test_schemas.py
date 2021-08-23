from api.schemas.users import UserAddress, UserAddress, UserMarketplace, UserBase


class TestSchemas:
    def test_user_base(self):
        pn = UserBase(fullname='hani rizo',
                      email='hanirizo@gmail.com',
                      password='pass124',
                      whatsapp="+68254545155",
                      online_store={})
        assert pn
        assert pn.whatsapp == '+68254545155'

    pass

    def test_user_marketplace(self):
        assert UserMarketplace(instagram="https://instagram.com")

    def test_users_address(self):
        assert UserAddress(nama='',
                           whatsapp='hanirizo@gmail.com',
                           provinsi=34,
                           provinsi_name='Yogyakarta',
                           kabupaten=3401,
                           kabupaten_name='Sleman',
                           kecamatan=340110,
                           kecamatan_name='Depok',
                           kelurahan=34011012,
                           kelurahan_name='Concat',
                           kodepos='55643',
                           alamat="jl macan no 1")
