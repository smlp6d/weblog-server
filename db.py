from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, update
from sqlalchemy import create_engine

from datetime import datetime
from time import time

from setup import sql_uri, debug, config
from db_declare import tables

from requests import get
from getpass import getuser

from hashlib import sha512
from random import randbytes
from base64 import b64encode


def gen_token():
    return b64encode(sha512(str(time()).encode('utf-8') + randbytes(20)).digest()).decode()


class db:
    def __init__(self):
        self.engine = create_engine(sql_uri, echo=debug)
        self.s = sessionmaker(bind=self.engine)()

    status = False

    def setup(self):
        ip4 = get('https://api.ipify.org').text
        ip6 = get('https://api64.ipify.org').text
        self.s.add(tables.turns(
            ip=ip4 + (' | ' + ip6) * (ip4 != ip6),
            user=getuser(),
            debug=debug,
            config=config.get_all()
        ))
        self.s.commit()
        self.status = True
        print('\r[ + ] db')

    def add_token(self, name):
        ans = self.s.execute(
            select(tables.tokens).where(tables.tokens.name == name, tables.tokens.alive == True)
        ).first()

        if ans:
            return 'name already exist'
        else:
            self.s.add(tables.tokens(name=name, token=gen_token()))
            self.s.commit()

            return f'token created for app : "{name}"'

    def get_token(self, name):
        ans = self.s.execute(
            select(tables.tokens).where(tables.tokens.name == name, tables.tokens.alive == True)
        ).first()

        if ans:
            return 'token:\n' + ans[0].__dict__['token'] + '\n'
        else:
            return 'token not found or not alive'

    def get_token_names(self):
        ans = ['\t' + b[0] for b in self.s.execute(self.s.query(tables.tokens.name)).all()][::-1]

        if ans:
            return 'tokens:\n' + '\n'.join(ans)
        else:
            return 'tokens not found or not alive'

    def add_login(self, addr):
        self.s.add(tables.logins(addr=f'{addr[0]}:{addr[1]}'))
        self.s.commit()

    def get_last_login(self):
        ans = self.s.query(tables.logins).order_by(tables.logins.id.desc()).first()
        if ans:
            return ans.__dict__['addr'], ans.__dict__['datetime'].strftime("%Y.%m.%d %X")
        else:
            return

    def get_last_logins(self, limit):
        ans = [
            [str(b.__dict__['id']), b.__dict__['addr'], b.__dict__['datetime'].strftime("%Y.%m.%d %X")]
            for b in self.s.query(tables.logins).order_by(tables.logins.id.desc()).limit(limit).all()
        ]
        return ans
