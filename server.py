import asyncio
import socket
from .Helper import Request,Response,Asset
from . import Config
from .Asyn import Asyn
from selectors import DefaultSelector,EVENT_READ

asyn = Asyn()

class Server(object):

    def __init__(self,host,port,dirpath=None):
        self.pool = {}
        self.cid_count = 0
        self.asset= Asset(dirpath) if dirpath else None
        self.sock = socket.socket()
        self.sock.setblocking(False)
        self.sock.bind((host,port))
        self.sock.listen(Config.QUENE_SIZE)

    def handler(self,c_sock,addr):
        try:
            with c_sock:
                data = yield from asyn.readall(c_sock)
                req = Request(data)
                res = Response(*self.asset.get(req.path))
                data = res.render()
                yield from asyn.sendall(c_sock,data)
        except Exception as e:
            raise e
    
    def close(self):
        self.sock.close()

    def start(self):
        try:
            asyn.listen(self.sock,self.handler)
            asyn.loop()
        except KeyboardInterrupt as e:
            print('Server stopped.')
            self.close()
        except Exception as e:
            print('Server stopped because of {error}'.format(error=str(e)))
            self.close()


