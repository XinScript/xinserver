import socket
from Helper import Request,Response,Asset
import Config
from Asyn import Asyn
from selectors import DefaultSelector,EVENT_READ
from logging import Logger,DEBUG


asyn = Asyn()
logger = Logger('logger',DEBUG)

class Server(object):

    def __init__(self,host,port,dirpath=None):
        self.pool = {}
        self.cid_count = 0
        self.asset= Asset(dirpath) if dirpath else None
        self.sock = socket.socket()
        self.sock.setblocking(False)
        self.sock.bind((host,port))
        self.sock.listen(Config.QUENE_SIZE)

    def handle(self,c_sock,addr):
        try:
            with c_sock:
                data = yield from asyn.readall(c_sock)
                req = Request(data)
                res = Response(*self.asset.get(req.path))
                data = res.render()
                yield from asyn.sendall(c_sock,data)
        
        except IndexError:
            with c_sock:
                c_sock.sendall(c_sock,Response.internal_error().render())
        
        except Exception as e:
            raise e
    
    def close(self):
        self.sock.close()

    def start(self):
        try:
            asyn.listen(self.sock,self.handle)
            logger.warning('Server Start.')
            asyn.loop()
        except KeyboardInterrupt as e:
            logger.warning('Server Stopped.')
            self.close()
        except Exception as e:
            logger.exception(e)
            self.close()



