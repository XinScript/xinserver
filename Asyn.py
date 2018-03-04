from selectors import DefaultSelector,EVENT_READ,EVENT_WRITE
from Future import Future
from MyRequest import Request
from MyResponse import Response
from Reader import Reader,Writer

class Asyn(object):

    _sel = DefaultSelector()

    def __init__(self):
        self.flag = True

    def accept(self,sock):
        fut = Future()
        self._sel.register(sock,EVENT_READ,(self._accept,fut))
        return (yield from fut)
        
    def _accept(self,sock,mask,fut):
        self._sel.unregister(sock)
        c_sock,addr = sock.accept()
        c_sock.setblocking(False)
        fut.set_result((c_sock,addr))

    def readall(self,c_sock):
        fut = Future()
        self._add_reader(c_sock,fut)
        return (yield from fut)

    def sendall(self,c_sock,data):
        fut = Future()
        self._add_writer(c_sock,fut,data)
        return (yield from fut)
        

    def _recv(self,c_sock,mask,fut,reader):
        chunk = c_sock.recv(100)
        reader.append(chunk)
        if len(chunk)!=100:
            self._remove_reader(c_sock)
            fut.set_result(reader.get_data())
    

    def _add_writer(self,c_sock,fut,data):
        writer = Writer(c_sock,data)
        self._sel.register(c_sock,EVENT_WRITE,(self._send,fut,writer))

    def _add_reader(self,c_sock,fut):
        reader = Reader(c_sock)
        self._sel.register(c_sock,EVENT_READ,(self._recv,fut,reader))

    def _remove_reader(self,c_sock):
        self._sel.unregister(c_sock)

    def _remove_writer(self, c_sock):
        self._sel.unregister(c_sock)

    def _send(self,c_sock,mask,fut,writer):
        writer.send()
        if writer.allsent:
            self._remove_writer(c_sock)
            fut.set_result(None)

    def loop(self):
        try:
            while True:
                events = self._sel.select()
                for key,mask in events:
                    cb,*args= key.data
                    cb(key.fileobj,mask,*args)
        except KeyboardInterrupt as e:
            raise e
        
            



