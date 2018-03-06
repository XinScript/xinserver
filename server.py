import sys
import asyncio
# from MyRequest import Request
# from MyResponse import Response
# from MyFile import File
from Helper import Request,Response,Asset
import Config
import socket
from Asyn import Asyn
from selectors import DefaultSelector,EVENT_READ
asyn = Asyn()

class Server(object):

    def __init__(self,host,port,dir_name):
        self.pool = {}
        self.cid_count = 0
        self.asset= Asset(dir_name)
        self.sock = socket.socket()
        self.sock.setblocking(False)
        self.sock.bind((host,port))
        self.sock.listen(Config.QUENE_SIZE)

    def handler(self,c_sock,addr):
        try:
            data = yield from asyn.readall(c_sock)
            req = Request(data)
            res = Response(*self.asset.get(req.path))
            data = res.render()
            yield from asyn.sendall(c_sock,data)
            c_sock.close()
        except Exception as e:
            raise e
    
    def _remove_task(self,cid):
        pass
        
    def close(self):
        self.sock.close()

    def start(self):
        try:
            asyn.listen(self.sock,self.handler)
            asyn.loop()
        except Exception as e:
            raise e

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('please make sure the format follows $dir $port.')
    else:
        hostname,port,rootdir = sys.argv[1],int(sys.argv[2]),sys.argv[3]
        server = Server(hostname,port,rootdir)
        server.start()


