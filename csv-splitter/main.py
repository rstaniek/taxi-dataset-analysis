import tmanager as tm
from sorter import DateSorter
import glob
from merger import ReMerger

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
    sort = DateSorter()
    args = dict()
    args['file'] = 'C:/Users/rajmu/Desktop/taxi-split/corrected/taxi_test.csv'
    args['thread'] = 'main-1'
    sort.split(args)

if __name__ == "__main__":
    merge()
    #test()
