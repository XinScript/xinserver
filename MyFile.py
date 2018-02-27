import os
import Common

class File(object):
    def __init__(self,dirname:str):
        self.dirname = os.path.realpath(os.path.join(os.getcwd(), dirname))

    def get(self, target: str)->tuple:
        c = bytes()
        path = os.path.realpath(''.join([self.dirname, target]))
        if path.find(self.dirname) != -1:
            if os.path.exists(path):
                if os.path.isdir(path):
                    names = ['..'] + os.listdir(path)
                    return '<br/>'.join(['<a href={path} style="font-size:1em;font-family:monospace;margin:10px;">{name}</a>'.format(name=name,path=os.path.join(target,name)) for name in names]).encode(),Common.OK
                else:
                    with open(path, 'rb') as f:
                        c = f.read()
                        return c,Common.OK
            else:
                return 'NOT FOUND.'.encode(),Common.NOT_FOUND
        else:
            return 'PERMISSION DENIED.'.encode(),Common.FORBIDDEN

