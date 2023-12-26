from threading import Thread
 
class CustomThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
 
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
             
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
 
""" 
def add(n1, n2):
    return n1 + n2
 
thread = CustomThread(target=add, args=(5, 3,))
thread.start()
print(thread.join())
"""