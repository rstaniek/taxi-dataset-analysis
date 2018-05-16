import tmanager as tm
from sorter import DateSorter
import glob
from merger import ReMerger
from distance_calc import Importer, Distance
from progress.bar import IncrementalBar
import time
import sys

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

def correlate(crime_file, taxi_file, output_prefix, output_path):
    csvlink = Importer()
    crimes = csvlink.import_crime(crime_file)
    taxis = csvlink.import_taxi(taxi_file)
    bar = IncrementalBar('Analyzing crime data', max=len(crimes), suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta_td)s')
    dist = Distance(1,0,1,0)# 1 day before, 1 day after

    print("Creating multi dimensional taxi array")
    filtered_taxi_list = dist.divide_into_days(taxis)
    print("Array created")
    
    result = list()
    ts = time.time()
    dist.get_taxis_per_crime(crimes, filtered_taxi_list, output_prefix, output_path)
    
    print("Quarter analyze done in " + str(time.time()-ts) + " seconds")



def main(args):
    #correlate(args[1], args[2], args[3], args[4])
    #crime files path, taxi files path, output prefix, output files path

    a1 = 'C:/Users/rajmu/Desktop/project-4/Crimes_by_quarter/crimes_only_significant_types-2013Q3.csv'
    a2 = 'C:/Users/rajmu/Desktop/project-4/cleaned/taxi-2013Q3.csv'
    a3 = '2013Q3'
    a4 = 'C:/Users/rajmu/Desktop/project-4/correlation/'
    correlate(a1,a2,a3,a4)
    

if __name__ == "__main__":
    #merge()
    #test()
    main(sys.argv)
