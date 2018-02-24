import os
class DirServ(object):
    def __init__(self,dirname:str):
        self.rootdir = rootdir = os.getcwd()
        self.dirname = os.path.realpath(os.path.join(rootdir,dirname))

    def serve(self, filename: str)->bytes:
        c = bytes()
        path = os.path.realpath(''.join([self.dirname, filename]))
        if path.find(self.rootdir) != -1:
            if os.path.exists(path):
                if os.path.isdir(path):
                    files = ['..'] + os.listdir(path)
                    return '<br/>'.join(['<a href={path} style="font-size:1em;font-family:monospace;margin:10px;">{path}</a>'.format(path=file) for file in files]).encode()
                else:
                    with open(path, 'rb') as f:
                        c = f.read()
                        return c
            else:
                return 'Path not exist.'.encode()
        else:
            return 'Permission denied.'.encode()


            
            
