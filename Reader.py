class Reader(object):
    def __init__(self,sock):
        self.data_cache = []
        self.sock = sock
    def append(self,chunk):
        self.data_cache.append(chunk)
    def get_data(self):
        return b''.join(self.data_cache)

class Writer(object):
    def __init__(self,sock,data):
        self.data = data
        self.sock = sock
        self.allsent = False

    def send(self):
        if self.allsent:
            pass
        else:
            n = self.sock.send(self.data)
            if n == len(self.data):
                self.allsent = True
            else:
                self.data = self.data[n:]


