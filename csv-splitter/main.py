import tmanager as tm
from sorter import DateSorter
import glob
from merger import ReMerger
from distance_calc import Importer, Distance

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
    path_to_taxi = 'C:/Users/rajmu/Desktop/project-4/cleaned/taxi-2017Q3.csv'
    path_to_crime = 'C:/Users/rajmu/Desktop/project-4/crime_dataset.csv'
    csvlink = Importer()
    crimes = csvlink.import_crime(path_to_crime)
    taxis = csvlink.import_taxi(path_to_taxi)
    dist = Distance('d200', 'd200')
    for x in range(10):
        k, v = dist.get_taxis_per_crime(crimes[x], taxis).popitem()
        print('{}: {}'.format(k, len(v)))


    

if __name__ == "__main__":
    #merge()
    #test()
    correlate()
