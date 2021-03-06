# XinServer
A event-based synchronous HTTP server based on python Selectors, Socket, Generator and self-implemented Future & Task.
## usage
serve static assets

	python xinserver hostname port dirpath
write your own handler
	
    import from xinserver.Server import Server

	class MyServer(Server):

    	def handler(self,c_sock,addr):

        	'''overwrite here'''
        	
## Classes


- Server
- Asyn - similar implementation asynchronous socket methods as provided by  [asyncio](https://docs.python.org/3/library/asyncio-eventloop.html#low-level-socket-operations)
- Future - represent the value generated by socket operation in the future, inspired by native python [Future](https://docs.python.org/3/library/concurrent.futures.html) & JavaScript Promise
- Co - generator behavior controller that enables to turn callback codes into sequential style, inspired by python [Task](https://docs.python.org/3/library/asyncio-task.html) & [Co](https://github.com/tj/co)
- Helper - simple encapsulation of handler in request, response, static assets server, reader and writer
- Common - common variables
- Config - configuration variables of the server including server name, buffer size etc.

## What else
- Notice that exceptions are not well handled
- All functionalities are pretty simple
- However it is a decent sample shows how to build a event-based asynchronous server