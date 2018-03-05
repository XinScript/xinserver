import sys
import asyncio
from MyRequest import Request
from MyResponse import Response
from MyFile import File
import Config
import socket
from Asyn import Asyn
from selectors import DefaultSelector,EVENT_READ
from Co import Co

selector = DefaultSelector()
asyn = Asyn()

class Server(object):
    queue_size = 1000
    def __init__(self,host,port,dir_name):
        self.pool = {}
        self.cid_count = 0
        self.file= File(dir_name)
        self.sock = socket.socket()
        self.sock.setblocking(False)
        self.sock.bind((host,port))
        self.sock.listen(1000)
        self.req_generator = self._req_generate()

    def handle(self):
        try:
            c_sock,addr = yield from asyn.accept(self.sock)
            next(self.req_generator)
            data = yield from asyn.readall(c_sock)
            req = Request(data)
            res = Response(*self.file.get(req.path))
            data = res.render()
            yield from asyn.sendall(c_sock,data)
        except Exception:
            pass
    
    # def readall(self, c_sock):
    #     data = []
    #     while True:
    #         chunk = yield from asyn.recv(c_sock, 4096)
    #         if not chunk:
    #             break
    #         else:
    #             data.append(chunk)
    #     return b''.join(data)
    def _remove_task(self,cid):
        pass
        
    def close(self):
        self.sock.close()

    def start(self):
        try:
            Co(self.handle())
            asyn.loop()
        except Exception as e:
            self.sock.shutdown(socket.SHUT_RDWR)
            raise e

    def _req_generate(self):
        while True:
            yield Co(self.handle())

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('please make sure the format follows $dir $port.')
    else:
        hostname,port,rootdir = sys.argv[1],int(sys.argv[2]),sys.argv[3]
        server = Server(hostname,port,rootdir)
        server.start()


