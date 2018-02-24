import socket
import sys
from io import StringIO
import time
import datetime
from req import Request
from response import Response
from dirServ import DirServ

class Server(object):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    quene_size = 1
    dir_name = '.'
    dir_sir = DirServ(dir_name)
    
    def __init__(self,server_address):
        self.listen_socket = listen_socket = socket.socket(self.address_family,self.socket_type)
        listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listen_socket.bind(server_address)
        listen_socket.listen(self.quene_size)
        host,port = listen_socket.getsockname()
        self.server_name = socket.getfqdn(host)
        self.server_port = port
    
    def serve(self):
        print('start listen.')
        while True:
            self.handle()
    
    def handle(self):
        try:
            client_connection,client_address = self.listen_socket.accept()
            request_data = client_connection.recv(1024).decode()
            req = Request(request_data)
            res = Response(self.dir_sir.serve(req.path))
            client_connection.sendall(res.render())
            client_connection.close()
        except Exception as e:
            print(e)
            client_connection.close()

if __name__ == '__main__':
    SERVER_ADDRESS = (HOST, PORT) = '', 8888
    server = Server(SERVER_ADDRESS)
    server.serve()


        

