
"""
Created on Feb 2, 2013

@author: derrick

This is a thread pool
"""
#from queue import deque #python 3.3
from collections import deque #python 2.7
from threading import Thread
from threading import Condition
from threading import Lock
from time import sleep
from include.log import Log


class Worker(Thread):
    """request new task to execute from ThreadPool"""

    def __init__(self, thread_pool, worker_id):
        """initial data and start myself as a new thread""" 
        Thread.__init__(self)
        self._pool          = thread_pool
        self._woker_id      = worker_id;
        self._is_dying      = False
        self._work_times    = 0
        self._rest_time     = 0.01
        self._log           = Log()
        

    def run(self):
        """ask and do works from task pool"""
        while (self._is_dying == False):
            """get the function name, parameter and the callback function"""
            func, args, callback = self._pool.get_new_task()      
            if func == None: #no task, have a rest
                sleep(self._rest_time)
            else:
                try:
                    """run the function with its parameter and the callback function"""
                    func(args, callback)
                except (Exception) as e:  
                    self._log.debug(e)
                    #sys.exit(1)
                ++self._work_times

    def goaway(self):
        """ stop myself, this lead to the end of the run function, which will kill the thread"""
        self._is_dying = True

class ThreadPool():
    """ Consuming tasks using threads in poll"""
    def __init__(self, threads_num, task_queue_max=None):
        self._threads_num   = threads_num
        self._tasks         = deque()
        self._threads       = []
        self._task_num      = 0
        self._task_lock     = Condition(Lock())
        self._thead_lock    = Condition(Lock())


    def start(self):
        """start all threads """
        self._thead_lock.acquire()
        try:
            for i in range(self._threads_num): 
                """start workers from here, pass itself as thread pool to the new started worker"""
                new_thread = Worker(self, i)
                self._threads.append(new_thread)
                new_thread.start()
        finally:
            self._thead_lock.release()

    def stop(self):
        #clear the task
        self._task_lock.acquire()
        try:
            self._tasks.clear(); 
        finally:
            self._task_lock.release()
            
        """stop all threads """
        self._thead_lock.acquire()
        try:
            for one_thread in self._threads: 
                one_thread.goaway()
            self._threads = []
            self._threads_num = 0
        finally:
            self._thead_lock.release()

      

    def queue_task(self, task, args, callback):
        self._task_lock.acquire()
        try:
            self._task_num += 1
            """the task queue store the function name, parameters and callback function"""
            self._tasks.append((task, args, callback))
        finally:
            self._task_lock.release()

    def get_new_task(self):
        self._task_lock.acquire()
        try:
            if (self._task_num <= 0):
                return ( None, None, None )
            else:
                self._task_num -= 1
                """pop out the new task and return"""
                return self._tasks.popleft()
        finally:
            self._task_lock.release()

    def get_queue_count(self):
        self._task_lock.acquire()
        try:
            return len(self._tasks)
        finally:
            self._task_lock.release()

    

#test
if __name__ == "__main__":

    def test_task1(num,callback):
        print("this is task 1: do {0}".format(num))
        callback()

    def test_task2():
        print("this is task 2")

    pool = ThreadPool(3, 10)

    pool.start()
    for i in range(10):  
        pool.queue_task(test_task1,i,test_task2)
        i += 1
    sleep(0.5)
    input('press any key to exit')
    pool.stop()

