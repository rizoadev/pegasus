import toml
from pathlib import Path
from libs.logs import Exc, Log


class Config:
    def load():
        exc = Exc.create_exception()
        Log(f'Load main ENV').send()

        try:

            envfile = Path.cwd().joinpath("env.toml")
            return toml.load(envfile)

        except Exception as e:
            # send exception msg
            exc.exception(e)
            return None
