import tmanager as tm
from sorter import DateSorter
import glob
from merger import ReMerger
from distance_calc import Importer, Distance
from progress.bar import IncrementalBar
import time

def split():
    #Fetch a list of files from a directory
    files = glob.glob('C:/Users/rajmu/Desktop/taxi-split/corrected/*.csv')
    for _i in range(len(files)):
        files[_i] = files[_i].replace('\\','/')
    
    #initialize thread managet
    manager = tm.ThreadManager(files)
    sort = DateSorter()
    manager.set_method_to_invoke(sort.split)
    manager.run()


def merge():
    path = 'C:/Users/rajmu/Desktop/taxi-split/corrected/by_quarter/*.csv'
    files = list()
    quarters = list()
    year = 2013
    q = 1
    for _i in range(20):
        quarters.append('{}Q{}'.format(str(year), str(q)))
        q += 1
        if (_i + 1) % 4 == 0:
            year += 1
            q = 1
    
    for _q in quarters:
        files_q = list(map((lambda x: x.replace('\\','/')), (_x for _x in glob.glob(path) if _q in _x)))
        files.append(files_q)

    manager = tm.ThreadManager(files, core_c=8)
    merger = ReMerger()
    manager.set_method_to_invoke(merger.merger)

    
    #manager.set_iterable_args(quarters)
    manager.run()
        



def test():

    #debug
    dist = Distance('h5', 'd3')
    print(dist.neighbours[45])


def correlate():
    path_to_taxi = 'C:/Users/1062085/Desktop/gudFiles/taxi-2017Q3.csv'
    path_to_crime = 'C:/Users/1062085/Desktop/gudFiles/Crimes2017Q3.csv'
    csvlink = Importer()
    crimes = csvlink.import_crime(path_to_crime)
    taxis = csvlink.import_taxi(path_to_taxi)
    bar = IncrementalBar('Analyzing crime data', max=len(crimes), suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta_td)s')
    dist = Distance(1,0,0,1)

    print("starting day division </3")
    filtered_taxi_list = dist.divide_into_days(taxis)
    
    print("finished day division <3")
    #for i in range(1,78):
     #   print(len(filtered_taxi_list[i]))
    #print(str(len(filtered_taxi_list[1])) + "yes")
    #print(len(filtered_taxi_list[77]))
    #print(len(filtered_taxi_list[8]))
    #print(len(filtered_taxi_list[32]))
    
    result = list()
    ts = time.time()
    for crime in crimes:
        k, v = dist.get_taxis_per_crime(crime, filtered_taxi_list).popitem()
        result.append('{}: {}'.format(k, len(v)))
        bar.next()
    
        #print(dist.get_taxis_per_crime(crimes[x], taxis))
        
    f = open("bamboozle.txt", "w+")
    
    for x in result:
        f.write(x + '\n')
    print(str(time.time()-ts) + " seconds")
    

if __name__ == "__main__":
    #merge()
    #test()
    correlate()
