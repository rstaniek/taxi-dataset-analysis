import tmanager as tm
from sorter import DateSorter
import glob

def main():
    #Fetch a list of files from a directory
    files = glob.glob('C:/Users/rajmu/Desktop/taxi-split/corrected/*.csv')
    for _i in range(len(files)):
        files[_i] = files[_i].replace('\\','/')
    
    #initialize thread managet
    manager = tm.ThreadManager(files)
    sort = DateSorter()
    manager.set_method_to_invoke(sort.split)
    manager.run()


def test():

    #debug
    sort = DateSorter()
    args = dict()
    args['file'] = 'C:/Users/rajmu/Desktop/taxi-split/corrected/taxi_test.csv'
    args['thread'] = 'main-1'
    sort.split(args)

if __name__ == "__main__":
    main()
    #test()
