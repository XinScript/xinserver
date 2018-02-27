import sys
import asyncio
from MyRequest import Request
from MyResponse import Response
from MyFile import File
import Config

loop = asyncio.get_event_loop()

class Server(object):

    def __init__(self,host,port,dir_name):
        self.file= File(dir_name)
        coro = asyncio.start_server(self.handle, host, port, loop=loop)
        self.server = loop.run_until_complete(coro)
    def start(self):
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        loop.run_until_complete(self.close())
        loop.close()
    
    async def handle(self,reader,writer):
        data = await self.readall(reader)
        req = Request(data)
        content, code = self.file.get(req.path)
        res = Response(content)
        res.set_code(code)
        writer.write(res.render())
        await writer.drain()
        writer.close()

    async def readall(self,reader):
        data = []
        chunk = await reader.read(Config.READ_BUF_SIZE)
        data.append(chunk)
        while len(chunk) == Config.READ_BUF_SIZE:
            chunk = await reader.read(Config.READ_BUF_SIZE)
            data.append(chunk)
        return b''.join(data)

    async def close(self):
        self.server.close()
        await self.server.wait_closed()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('please make sure the format follows $dir $port.')
    else:
        hostname,port,rootdir = sys.argv[1],int(sys.argv[2]),sys.argv[3]
        server = Server(hostname,port,rootdir)
        server.start()


