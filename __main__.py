import sys
from Server import Server

if len(sys.argv) != 4:
    print('Please make sure the arguments correct:$hostname $port $dirpath')
else:
    host, port, dirpath = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    print(host,port,dirpath)
    server = Server(host, port, dirpath)
    server.start()
