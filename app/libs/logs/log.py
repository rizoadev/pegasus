# Log listener
#
# Copyright (c) Riza Masykur 2021.
#
# History:
# 0.1   17-08-21 yk     Created

# import logging
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Log:
    msg: str

    def send(self):
        d = f"{datetime.now()} - {self.msg}"
        CRED = '\33[3m\33[32m'
        CREN = '\033[0m'
        print(CRED + d + CREN)