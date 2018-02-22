import socket
import sys
from io import StringIO
import time
import datetime
from req import Request

class Server(object):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    quene_size = 1
    
    def __init__(self,server_address):
        self.listen_socket = listen_socket = socket.socket(self.address_family,self.socket_type)
        listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listen_socket.bind(server_address)
        listen_socket.listen(self.quene_size)
        host,port = self.listen_socket.getsockname()
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.headers = []
    
    def set_app(self,application):
        self.application = application
    
    def serve(self):
        print('start listen.')
        while True:
            self.client_connection,client_address = self.listen_socket.accept()
            self.handle()
    
    def handle(self):
        request_data = self.client_connection.recv(1024)
        [print(line.decode('utf-8')) for line in request_data.splitlines()]
        req = Request(request_data)
        env = self.get_environ(req)
        exit(0)

    def get_environ(self,req):
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = StringIO(req.input)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = req.method    # GET
        env['PATH_INFO']         = req.path              # /hello
        env['SERVER_NAME']       = self.server_name       # localhost
        env['SERVER_PORT']       = str(self.server_port)  # 8888
        return env

    def start_response(self, status, response_headers, exc_info=None):
        # Add necessary server headers
        server_headers = [
            ('Date', datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")),
            ('Server', 'XINSERVER 1.0'),
        ]
        self.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. We simplicity's sake we'll ignore that detail
        # for now.
        # return self.finish_response

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data
            # Print formatted response data a la 'curl -v'
            print(''.join(
                '> {line}\n'.format(line=line)
                for line in response.splitlines()
            ))
            self.client_connection.sendall(response)
        finally:
            self.client_connection.close()

if __name__ == '__main__':
    print()
    # SERVER_ADDRESS = (HOST, PORT) = '', 8888
    # server = Server(SERVER_ADDRESS)
    # server.serve()


        

