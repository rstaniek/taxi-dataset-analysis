import time
import math

start = time.time()

s = 0.0032535

def normal(x):
    start = time.time()
    for i in range(0,x):
        t = math.sin(s) * math.sin(s)
    print(str(time.time() - start) + " seconds for x*x doing " + str(x) + " iterations")


def stars(x):
    start = time.time()
    for i in range(0,x):
        t = math.sin(s) ** 2
    print(str(time.time() - start) + " seconds for x**2 doing " + str(x) + " iterations")


def mathpow(x):
    start = time.time()
    for i in range(0,x):
        t = math.pow(math.sin(s), 2)
    print(str(time.time() - start) + " seconds for math.pow(x, 2) doing " + str(x) + " iterations")


def bitshift(x):
    start = time.time()
    for i in range(0,x):
        t = math.sin(s) >> 2
    print(time.time() - start + " seconds for x>>2 doing " + x + " iterations")
    

def powsmol(x):
    start = time.time()
    for i in range(0,x):
        t = math.sin(s) ** .5
    print(str(time.time() - start) + " seconds for x**.5 doing " + str(x) + " iterations")
    

def squirt(x):
    start = time.time()
    for i in range(0,x):
        t = math.sqrt(s)
    print(str(time.time() - start) + " seconds for math.sqrt() doing" + str(x) + " iterations")
    
    

def run_me_daddy(x):
    print("x is math.sin()")
    #normal(x)
    #stars(x)
    #mathpow(x)
    powsmol(x)
    squirt(x)

#run_me_daddy(1000)
#run_me_daddy(10000)
#run_me_daddy(100000)
#run_me_daddy(1000000)
#run_me_daddy(1000000)
#run_me_daddy(1000000)
#run_me_daddy(10000000)


new_list = list()
g = globals()
for i in range(1,78):
    g["taxi_com{0}".format(i)] = list()
    new_list.append(g['taxi_com' + str(i)])
x = list()
x.append("asd")
x.append(34)
#g[taxi_com4][0] = x
#print(g[taxi_com4])
new_list[4].append(x)
print(new_list)