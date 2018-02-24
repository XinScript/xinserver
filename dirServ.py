import os
class DirServ(object):
    def __init__(self,dirname:str):
        self.dirname = os.path.realpath(os.path.join(os.getcwd(), dirname))

    def serve(self, target: str)->bytes:
        c = bytes()
        path = os.path.realpath(''.join([self.dirname, target]))
        if path.find(self.dirname) != -1:
            if os.path.exists(path):
                if os.path.isdir(path):
                    names = ['..'] + os.listdir(path)
                    return '<br/>'.join(['<a href={path} style="font-size:1em;font-family:"Lucida Sans";margin:10px;">{name}</a>'.format(name=name, path=os.path.join(target, name)) for name in names]).encode()
                else:
                    with open(path, 'rb') as f:
                        c = f.read()
                        return c
            else:
                return 'Path not exist.'.encode()
        else:
            return 'Permission denied.'.encode()
