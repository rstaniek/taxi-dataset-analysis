import threading
import multiprocessing
import numpy as np
import time
from datetime import datetime


class ThreadRunException(Exception):
    def __init__(self, message, errors=None):
        super(Exception, self).__init__(message)
        self.errors = errors


class ProcessThread(threading.Thread):
    def __init__(self, threadID, name, file, callback):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.file = file
        self.callback = callback
        self.method = None
        self.method_args = None


    def set_file(self, file):
        #check if thread is not executing now
        if not self.isAlive():
            self.file = file
        else:
            raise ThreadRunException('Thread is currently running! Cannot change the source file.', self.name)


    def method_set(self, value):
        self.method = value


    def method_args_set(self, kwargs):
        self.method_args = kwargs


    def run(self):
        if self.method_args is None:
            self.method_args = dict()
        self.method_args['file'] = self.file
        self.method_args['thread'] = self.name
        #execute the injected method with a parameters passed as a dictionary
        self.method(self.method_args)
        #when the work is done
        self.callback(self.threadID)


class ThreadManager:

    THREAD_CHECK_INTERVAL = 0.5

    def __init__(self, files, method_to_invoke=None, method_args=None, core_c=None, iterable_args=None):
        print('Initliailzing thread manager...')
        if core_c is None:
            self.CORE_COUNT = int(multiprocessing.cpu_count())
        else:
            self.CORE_COUNT = core_c
        self.avail_threads = list()
        self.working_threads = list()
        self.file_stack = files
        self.method_to_invoke = method_to_invoke
        if iterable_args is None:
            self.iterable_args = None
        else:
            self.iterable_args = iterable_args
        if method_args is None:
            self.method_args = dict()
        else:
            self.method_args = method_args
        #self.method_args['files'] = self.file_stack

        for _i in range(self.CORE_COUNT):
            self.avail_threads.append(
                ProcessThread(_i, 
                              'processThread-%d' % _i, 
                              None, 
                              self.__on_thread_finished__))
        print('Thread Manager initialized.')



    def set_method_to_invoke(self, method):
        self.method_to_invoke = method


    def set_method_args(self, kwargs):
        self.method_args = kwargs


    def set_iterable_args(self, args):
        self.iterable_args = args


    @property
    def task_count(self):
        return len(self.file_stack)


    def __str__(self):
        return '[{}] Process running...\nThread count: {}\nThreads active: {}\nTasks to process: {}'.format(str(datetime.now()), self.CORE_COUNT, len(self.working_threads), self.task_count)


    #a callback invoked when a certain thread is finished with its tasks.
    #sends back ID for further identification in the manager
    def __on_thread_finished__(self, id):
        #release a thread from the worker list and push it to idle list
        thread = next(t for t in self.working_threads if id == t.threadID)
        self.working_threads.remove(thread)
        del thread
        #reinstantiate a new thread with the same ID after deleting the previous one
        self.avail_threads.append(ProcessThread(id, 'processThread-%d' % id, None, self.__on_thread_finished__))
        print('[{}] Thread #{} has exited its process\nTHREADS IDLE: {}\nTHREADS ACTIVE: {}\nTasks left: {}'.format(str(datetime.now()), id, len(self.avail_threads), len(self.working_threads), self.task_count))


    def __assign_tasks__(self):
        #while there are still files on the stack
        if len(self.file_stack) > 0:
            #while there are still threads available
            while len(self.avail_threads) > 0 and self.task_count > 0:
                thread = self.avail_threads.pop()
                thread.method_set(self.method_to_invoke)
                if self.iterable_args is not None:
                    arg = self.iterable_args.pop()
                    self.method_args['iterable'] = arg
                thread.method_args_set(self.method_args)
                try:
                    #pop a file from a stack and assign it to a process
                    file = self.file_stack.pop()
                    thread.set_file(file)
                    print('File {} assigned to thread: {}'.format(file, thread.name))
                except ThreadRunException as ex:
                    print(ex)
                #start the thread
                thread.start()
                #add it to the list of working threads
                self.working_threads.append(thread)


    def run(self):
        #run a loop until we processed all the requests
        while self.task_count > 0:
            #print info status
            #if int(datetime.now().strftime('%S')) % 30 == 0:
                #print(self.__str__())
            time.sleep(ThreadManager.THREAD_CHECK_INTERVAL)
            #assign tasks to the lazy idle bastards
            self.__assign_tasks__()
        print('All tasks have been assigned')
        print(self.__str__())
        while len(self.working_threads) > 0:
            time.sleep(ThreadManager.THREAD_CHECK_INTERVAL)
        print('All threads have finished')
        print(self.__str__())
            
