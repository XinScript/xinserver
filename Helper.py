import datetime
from . import Config
from . import Common
import os


class Response(object):
    def __init__(self, body, code=Common.OK):
        self.body = body
        self.code = code
        self.header = header = {}
        header['Date'] = datetime.datetime.utcnow(
        ).strftime(Config.DATE_FORMAT)
        header['Server'] = Config.SERVER_NAME
        self._clean()
        header['Content-Length'] = str(len(self.body))

    def set_code(self, code):
        self.code = code
        return self

    def render(self)->bytes:
        status = 'HTTP/{version} {code}\r\n'.format(
            version=Config.VERSION, code=self.code)
        header = ''.join(
            [k + ': ' + v + '\r\n' for k, v in self.header.items()])
        http_info = status + header + '\r\n'
        return b''.join([http_info.encode(), self.body])
    
    def _clean(self):
        if self.code == Common.FORBIDDEN:
            self.body = 'Permission Denied.'.encode()
        elif self.code == Common.NOT_FOUND:
            self.body = 'Not Found.'.encode()
        elif self.code == Common.INTERNAL_SERVER_ERROR:
            self.body = 'Server Internal Error.'.encode()

    @classmethod
    def internal_error(cls):
        return Response('Server Internal Error.'.encode(),500)





class Request(object):
    def __init__(self, data):
        self.data = data
        try:
            lines = data.decode().rstrip('\r\n').splitlines()
            self.method, self.path, self.protocol = lines[0].rstrip(
                '\r\n').split()
            self.info = {k.lower(): v for k, v in [
                line.split(':', 1) for line in lines[1:]]}
        except Exception as e:
            raise e

    def __str__(self):
        return self.data.decode()


class Reader(object):
    def __init__(self, sock):
        self.data_cache = []
        self.sock = sock

    def append(self, chunk):
        self.data_cache.append(chunk)

    def get_data(self)->bytes:
        return b''.join(self.data_cache)


class Writer(object):
    def __init__(self, sock, data):
        self.data = data
        self.sock = sock
        self.allsent = False

    def send(self)->int:
        if self.allsent:
            return 0
        else:
            n = self.sock.send(self.data)
            if n == len(self.data):
                self.allsent = True
            else:
                self.data = self.data[n:]
            return n


class Asset(object):
    def __init__(self, dirname: str):
        self.dirname = os.path.realpath(os.path.join(os.getcwd(), dirname))

    def get(self, target: str)->tuple:
        content,code = b'',Common.OK
        path = os.path.realpath(''.join([self.dirname, target]))
        if path.find(self.dirname) != -1:
            if os.path.exists(path):
                if os.path.isdir(path):
                    names = ['..'] + os.listdir(path)
                    file_style = '"font-size:1em;font-family:monospace;margin:10px;color:blue;"'
                    dir_style = '"font-size:1em;font-family:monospace;margin:10px;color:green;"'
                    return '<br/>'.join(['<a href={path} style={style}>{name}</a>'.format(name=name, style=dir_style if os.path.isdir(path+'/'+name) else file_style, path=os.path.join(target, name)) for name in names]).encode(), Common.OK
                else:
                    with open(path, 'rb') as f:
                        content = f.read()
            else:
                code = Common.NOT_FOUND
        else:
            code = Common.FORBIDDEN
        return content,code