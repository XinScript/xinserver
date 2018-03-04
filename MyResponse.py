import datetime
import Config
import Common

class Response(object):
    def __init__(self,body:bytes,code):
        self.header = header = {}
        header['Date'] = datetime.datetime.utcnow(
        ).strftime(Config.DATE_FORMAT)
        header['Server'] = Config.SERVER_NAME
        self.body = body
        header['Content-Length'] = str(len(self.body))
        self.set_code(Common.OK)

    def set_code(self,code):
        self.code = code
        
    def render(self)->bytes:
        status = 'HTTP/{version} {code}\r\n'.format(version=Config.VERSION,code=self.code)
        header = ''.join([k + ': ' + v + '\r\n' for k, v in self.header.items()])
        http_info = status + header + '\r\n'
        return b''.join([http_info.encode(),self.body])