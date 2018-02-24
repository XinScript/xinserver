import datetime
class Response(object):
    def __init__(self,body):
        self.header = header = {}
        header['Date'] = datetime.datetime.utcnow(
        ).strftime("%a %b %d %H:%M:%S %Z %Y")
        header['Server'] = 'xinserver'
        self.body = body if isinstance(body,bytes) else body.encode()
    def render(self)->bytes:
        status = 'HTTP/1.1 200 OK\r\n'
        header = ''.join([k + ': ' + v + '\r\n' for k, v in self.header.items()])
        http_info = status + header + '\r\n'
        return b''.join([http_info.encode(),self.body])


        
