import time
import math
import sys
import datetime

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


#new_list = list()
#g = globals()
#for i in range(1,78):
#    g["taxi_com{0}".format(i)] = list()
#    new_list.append(g['taxi_com' + str(i)])
#x = list()
#x.append("asd")
#x.append(34)
#g[taxi_com4][0] = x
#print(g[taxi_com4])
#new_list[4].append(x)
#print(new_list)




def gen_list(x):
    start = time.time()
    for i in range(0,x):
        t = list()
    print(str(time.time() - start) + " seconds for " + str(x) + " lists created")

def gen_array(x):
    start = time.time()
    for i in range(0,x):
        t = []
    print(str(time.time() - start) + " seconds for " + str(x) + " arrays created\n")
    

def get_index(x):
    start = time.time()
    for i in range(20,x):
        t = [i for i in range(0,1000)]
        y = t.index(7)
    print(str(time.time() - start) + " seconds for " + str(x) + " arrays created")
   
def bop_index(x):
    start = time.time()
    for i in range(20,x):
        t = [i for i in range(0,1000)]
        y = t[7]
    print(str(time.time() - start) + " seconds for " + str(x) + " arrays created\n")
 

def cunt_destroyer():
    gen_list(10000)
    gen_array(10000)
    gen_list(100000)
    gen_array(100000)
    gen_list(1000000)
    gen_array(1000000)
    gen_list(10000000)
    gen_array(10000000)

def cock_buster():
    get_index(1000)
    bop_index(1000)
    get_index(10000)
    bop_index(10000)
    get_index(100000)
    bop_index(100000)


def divide_my_ass():
    g = globals()
    s = [i for i in range(0,100)]
    t = []
    for i in range(0,10):
        t.append([j for j in range(1*10*i,(1+i)*10)])
    print(str(sys.getsizeof(s)) + " 10000 items in a array")
    print(str(sys.getsizeof(t)) + " 100 items in 100 arrays, nested")
    print(str(sys.getsizeof([j for j in range(50,60)])) + " 100 items in 100 arrays, nested")
    print(s)
    print(t)

#cunt_destroyer()
#cock_buster()
#divide_my_ass()
def get_quarter_day(date):
    dayss = {1: 31,
             2: 29,
             3: 31,
             4: 30,
             5: 31,
             6: 30,
             7: 31,
             8: 31,
             9: 30,
             10: 31,
             11: 30,
             12: 31}
    x = date
    qd = 0
    #x = datetime.date.today()
    m = x.month
    n = m
    while m > 0:
        if m // 3 > 0:
            qd = qd + dayss[n]
        m =  m // 3
    qd = qd + x.day
    return qd

def nth_quarter_day(date):
    q_size = { 1: 89, 2: 89, 3: 90,
               4: 91, 5: 92, 6: 91,
               7: 93, 8: 93, 9: 93,
               10: 93, 11: 93, 12: 93}
    new_year_day = datetime.datetime(year=date.year, month=1, day=1)
    return ((date - new_year_day).days + 1) % q_size[date.month]

#print(get_quarter_day(datetime.datetime.strptime('28-01-2018', '%d-%m-%Y')))
#print(nth_quarter_day(datetime.datetime.strptime('01-01-2017', '%d-%m-%Y')))
#print(nth_quarter_day(datetime.datetime.strptime('31-03-2017', '%d-%m-%Y')))
#print(nth_quarter_day(datetime.datetime.strptime('01-04-2017', '%d-%m-%Y')))
#print(nth_quarter_day(datetime.datetime.strptime('30-06-2017', '%d-%m-%Y')))
#print(nth_quarter_day(datetime.datetime.strptime('01-07-2017', '%d-%m-%Y')))
#print(nth_quarter_day(datetime.datetime.strptime('30-09-2017', '%d-%m-%Y')))
#print(nth_quarter_day(datetime.datetime.strptime('01-10-2017', '%d-%m-%Y')))
#print(nth_quarter_day(datetime.datetime.strptime('31-12-2017', '%d-%m-%Y')))

x = ["muee"]
y = ["muitsa"]
z = ["ecstra mue"]

y.append(x)
z.append(y)


#print (z)


cartofel = [ [[[[i+j+k]for k in range(0,32)]] for j in range(0,3)] for i in range(0,5)]
cc = [ [ [ [i+j+k] for k in range(0,32) ] for j in range(0,3) ] for i in range(0, 78)] 
print (cc[0][0][0])


