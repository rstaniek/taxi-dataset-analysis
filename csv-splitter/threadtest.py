import time
from utils import Executable

class ThreadTester(Executable):
    def run(self, args):
        number = args['file']
        thread = args['thread']
        if number < 0:
            raise ValueError('Cannot process a negative number!')
        start_t = time.time()
        #result = self.__fib__(number)[0]
        result = self.__fib_slow(number)
        delta_t = time.time() - start_t
        print('{} is exiting... Time elapsed: {}s'.format(thread, delta_t))


    def __fib__(self, num):
        if num == 0:
            return (0, 1)
        else:
            a, b = self.__fib__(num // 2)
            c = a * (b * 2 - a)
            d = (a * a) + (b * b)
            if num % 2 == 0:
                return (c, d)
            else:
                return (d, c + d)


    def __fib_slow(self, num):
        if num == 0:
            return 0
        elif num == 1:
            return 1
        else:
            return self.__fib_slow(num - 1) + self.__fib_slow(num - 2)


