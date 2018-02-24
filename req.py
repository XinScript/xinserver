class Request(object):
    def __init__(self,data):
        self.data = data
        try:
            print('being')
            print(data)
            # print(self.path)
            lines = data.rstrip('\r\n').splitlines()
        # [print(line)for line in lines]
            self.method,self.path,self.protocol = lines[0].rstrip('\r\n').split()
            self.info = {k.lower(): v for k, v in [line.split(':', 1) for line in lines[1:]]}
        except Exception as e:
            print(e)
            
    def __str__(self):
        return self.data
    
