from Future import Future
class Co(object):
    def __init__(self,coro):
        f = Future()
        f.set_result(None)
        self.coro = coro
        self.next_step(f)

    def next_step(self,future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.next_step)
    
        
