import tmanager as tm
from sorter import DateSorter
import glob
from merger import ReMerger
from distance_calc import Importer, Distance
from progress.bar import IncrementalBar

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
    path_to_crime = 'C:/Users/rajmu/Desktop/project-4/Crimes_by_quarter/Crimes2017Q3.csv'
    csvlink = Importer()
    crimes = csvlink.import_crime(path_to_crime)
    taxis = csvlink.import_taxi(path_to_taxi)
    bar = IncrementalBar('Modelling Taxi Trips', max=len(crimes), suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta_td)s')
    dist = Distance('h1', 'd1')

    result = list()
    for crime in crimes:
        k, v = dist.get_taxis_per_crime(crime, taxis).popitem()
        result.append('{}: {}'.format(k, len(v)))
        bar.next()

        #print(dist.get_taxis_per_crime(crimes[x], taxis))
    for x in result:
        print(x)


def correlate_threaded():
    path_to_taxi = 'C:/Users/rajmu/Desktop/project-4/cleaned/taxi-2017Q3.csv'
    path_to_crime = 'C:/Users/rajmu/Desktop/project-4/Crimes_by_quarter/Crimes2017Q3.csv'
    out_path_template = 'C:/Users/rajmu/Desktop/project-4/correlation/2017Q3-{}.csv'
    args = list()
    loader = Importer()
    crimes = loader.import_crime(path_to_crime)
    crimes_partitioned = loader.partition(crimes)
    taxis = loader.import_taxi(path_to_taxi)

    for part in crimes_partitioned:
        _dict = dict()
        _dict['crime_list'] = part
        _dict['taxi_list'] = taxis
        _dict['out_path'] = out_path_template
        args.append(_dict)

    manager = tm.ThreadManager(args)
    distance = Distance('h1', 'd2')
    manager.set_method_to_invoke(distance.run)

    manager.run()

    

if __name__ == "__main__":
    #merge()
    #test()
    correlate_threaded()
