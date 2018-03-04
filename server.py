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

    def __init__(self,host,port,dir_name):
        self.file= File(dir_name)
        self.sock = socket.socket()
        self.sock.setblocking(False)
        self.sock.bind((host,port))
        self.sock.listen(1000)
        self.req_generator = self._req_generate()

    def handle(self):
        c_sock,addr = yield from asyn.accept(self.sock)
        data = yield from asyn.readall(c_sock)
        req = Request(data)
        res = Response(*self.file.get(req.path))
        data = res.render()
        yield from asyn.sendall(c_sock,data)
        self.close()
        
    def close(self):
        self.sock.close()

    def start(self):
        for i in range(5):
            Co(self.handle())
        try:
            asyn.loop()
        except KeyboardInterrupt:
            self.sock.close()
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


