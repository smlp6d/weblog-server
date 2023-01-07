from setup import port, addr, const_key, key_size, key_file, package_max_size
from db import db as db_base
from time import strftime
import socket
from mpsp import mps
import threading

from modules import user

db = db_base()


def router(sock, addr):
    p = mps(
        sock, package_max_size=package_max_size,
        key_size=key_size, const_key=const_key, key_file=key_file
    )
    assert p.set_handshake()

    mode = p.recv()

    print(f'connected [{mode}] :  {addr[0]}:{addr[1]}')

    send, recv = p.send, p.recv

    if mode == 'user':
        user(send, recv, addr)
    else:
        send('err')

    p.close()


if __name__ == '__main__':
    print(f'[   ] db', end='')
    db.setup()

    print('[   ] server', end='')
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((addr, port))
    s.listen()
    print('\r[ + ] server')

    print('[   ] pgen', end='')
    pgen = mps(None, const_key=const_key, key_size=key_size, key_file=key_file)
    print(f'\r[ + ] pgen {pgen.calc_pub_sha()}\n')

    print(f't> {strftime("%Y.%m.%d %X")}  ap> {addr}:{port}\n')

    while True:
        sock, addr = s.accept()

        tread = threading.Thread(target=router, args=(sock, addr))
        tread.start()
