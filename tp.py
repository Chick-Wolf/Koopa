from typing import Callable, Any, Iterable

from threading import Thread
from time import sleep

class Task:
    
    # TODO: Put some generics?
    func:   Callable
    args:   tuple[tuple[Iterable[Any],dict]]
    result: dict[int,Any]
    
    def __init__( self, func: Callable, args: tuple[tuple[Iterable[Any],dict]] ):
        self.func = func
        self.args = args
        self.result = {}
        
    def wait_for_all( self ) -> list:
        n = len(self.args)
        while len(self.result) < n:
            sleep(.05)
        return [self.result[i] for i in range(n)]

class Submission:
    
    task: Task
    i:    slice
    
    def __init__( self, task: Task, i: slice ):
        self.task = task
        self.i = i

class TP:
    
    # TODO: Unify into a single list of tuple (tuple[tuple[Thread,list[Submission]],...])
    pool:   tuple[Thread,...]
    queues: tuple[list[Submission],...]
    
    def __init__( self, size: int ):
        self.queues = tuple([] for _ in range(size))
        self.pool = tuple(Thread(target=_tp_fn,args=(self,i,self.queues[i])) for i in range(size))
        
    def start( self ):
        for t in self.pool:
            t.start()
            
    def submit( self, task: Task ):
        for i, q in enumerate(self.queues):
            q.append(Submission(task,slice(i,None,len(self.queues))))

def _tp_fn(tp: TP, i: int, q: list[Submission]):
    from time import sleep
    while True:
        sleep(.001)
        while len(q):
            s = q.pop(0)
            # TODO: Don't iterate over every single argument to find the right ones
            for j, (args,kwargs) in list(enumerate(s.task.args))[s.i]:
                s.task.result[j] = s.task.func(*args,**kwargs)

# (temporary)
# Example usage:
"""
from tp import TP, Task

def add( a, b ):
    return a + b

tp = TP(4)

t = Task(add,(
    ((1,2,),{}),
    ((3,4,),{})    
))

tp.submit(t)
tp.start()

print(t.wait_for_all())
"""
