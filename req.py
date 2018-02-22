class Request(object):
    def __init__(self,blines):
        self.input = blines
        lines = blines.decode('utf-8').rstrip('\r\n').splitlines()
        self.method,self.path,self.protocol = lines[0].rstrip('\r\n').split()
        self.info = {k.lower(): v for k, v in [line.split(':', 1) for line in lines[1:]]}
