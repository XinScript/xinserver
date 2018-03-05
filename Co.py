from Future import Future
class Co(object):
    def __init__(self,coro,cid=None):
        f = Future()
        f.set_result(None)
        self.coro = coro
        self.next_step(f)
        self.isdone = False
        self.cid = cid

    def next_step(self,future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            self.isdone = True
        # except Exception
        else:
            next_future.add_done_callback(self.next_step)

    def done(self):
        return self.isdone
    
        
