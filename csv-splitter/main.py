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
    manager.set_method_to_invoke(DateSorter.split)
    manager.run()

if __name__ == "__main__":
    main()
