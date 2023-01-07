from json import dumps
from time import sleep
from random import random
from setup import pass_hash, default_limit
from server import db


def user_app(out, inp):
    limit = default_limit
    while True:
        com = inp('u>_').strip()
        cse = com.split(' ')

        if com == 'q' or com == 'exit':
            out('bye!')
            break
        elif com == 'help' or com == 'h':
            out('commands:\nhelp  [ h ]\ncreate <name>\nget <name>\nlist\nlogins\nlimit [ l ]')
        elif com == 'list':
            out(db.get_token_names())
        elif com == 'logins':
            out('\n'.join([' \t'.join(b) for b in db.get_last_logins(limit)]))
        elif com == 'l' or com == 'limit':
            lim = inp(f'set limit[{limit}]:_')
            if (lim.isdigit() or lim[1:].isdigit() and lim[0] == '-') and lim != '0':
                limit = int(lim)
                out(f'limit set {limit}')
            elif lim == '' or lim == 'q':
                out('limit not set')
            else:
                out(f'limit not set  incorrect input : "{lim}"')
        elif com == '':
            pass
        elif len(cse) == 2:
            if cse[0] == 'create':
                out(db.add_token(cse[1]))
            elif cse[0] == 'get':
                out(db.get_token(cse[1]))
            else:
                out(f'unknown command : "{com}"')
        elif com in ['create', 'get']:
            out(f'wrong argument number ({len(cse)}) "{com}"')
        else:
            out(f'unknown command : "{com}"')


def user(send, recv, addr):
    send('ok')

    def out(*objects, sep='', end='\n'):
        send(dumps(
            {'fun': 'out', 'data': {'obj': objects, 'tup': type(objects) is tuple, 'sep': sep, 'end': end}}
        ))
        recv()

    def inp(text=''):
        send(dumps({'fun': 'inp', 'data': {'txt': text}}))
        return recv()

    acc = False
    while not acc:
        rcv = recv()
        if rcv == pass_hash:
            send('ok')
            acc = True
        elif rcv == 'q':
            send('ex')
            break
        else:
            sleep(random() * 2)
            send('er')

    if acc:
        ll = db.get_last_login()
        if ll:
            llf = ' at '.join(ll)
        else:
            llf = '-'

        out(f'#correct\n#last login from {llf}')
        db.add_login(addr)
        user_app(out, inp)
        send(dumps({'fun': 'end'}))
