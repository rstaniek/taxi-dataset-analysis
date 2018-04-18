import threading


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


    @property
    def id(self):
        return self.threadID


    @property
    def method(self):
        return self.method


    @property
    def name(self):
        return self.name


    @property
    def method_args(self):
        return self.method_args


    @method.setter
    def method(self, value):
        self.method = value


    @method_args.setter
    def method_args(self, **kwargs):
        self.method_args = kwargs


    def run(self):
        #TODO: to be implemented

        #when the work is done
        self.callback(self.threadID)


class ThreadManager:
    import multiprocessing
    import numpy as np
    import time

    THREAD_CHECK_INTERVAL = 0.5

    def __init__(self, files, method_to_invoke=None, method_args=None):
        self.CORE_COUNT = int(multiprocessing.cpu_count())
        self.avail_threads = list()
        self.working_threads = list()
        self.file_stack = files
        self.method_to_invoke = method_to_invoke
        self.method_args = method_args

        for _i in range(self.CORE_COUNT):
            self.avail_threads.append(
                ProcessThread(_i, 
                              'processThread-%d' % _i, 
                              None, 
                              self.__on_thread_finished__))


    @property
    def method_to_invoke(self):
        return self.method_to_invoke


    @method_to_invoke.setter
    def method_to_invoke(self, value):
        self.method_to_invoke = value


    @property
    def method_args(self):
        return self.method_args


    @method_args.setter
    def method_args(self, **kwargs):
        self.method_args = kwargs


    @property
    def task_count(self):
        return len(self.file_stack)


    def __str__(self):
        return 'ThreadManager class: {}\nThread count: {}\nTasks to process: {}'.format(self.__repr__, self.CORE_COUNT, len(self.file_stack))


    #a callback invoked when a certain thread is finished with its tasks.
    #sends back ID for further identification in the manager
    def __on_thread_finished__(self, id):
        #release a thread from the worker list and push it to idle list
        thread = next(t for t in self.working_threads if id == t.id)
        self.working_threads.remove(thread)
        self.avail_threads.append(thread)
        print('Thread #{} has exited its process\nTHREADS IDLE: {}\nTHREADS ACTIVE: {}'.format(id, len(self.avail_threads), len(self.working_threads)))


    def __assign_tasks__(self):
        #while there are still threads available
        while len(self.avail_threads) > 0:
            thread = self.avail_threads.pop()
            thread.method = self.method_to_invoke
            thread.method_args = self.method_args
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
            time.sleep(ThreadManager.THREAD_CHECK_INTERVAL)
            #assign tasks to the lazy idle bastards
            self.__assign_tasks__()
        print('All tasks have been assigned')
        while len(self.working_threads) > 0:
            time.sleep(ThreadManager.THREAD_CHECK_INTERVAL)
        print('All threads have finished')
            
