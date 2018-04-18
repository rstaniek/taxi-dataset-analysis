import pandas as pd
import numpy as np
from progress.bar import ShadyBar
import sys
import threading

class SplitThread(threading.Thread):
    def __init__(self, threadID, name, file_num):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.file_num = file_num


    def run(self):
        print('Starting {} for file #{}...'.format(self.name, self.file_num))
        print('[{}] Loading data frame #{}...'.format(self.name, self.file_num))
        df = pd.read_csv(file_path % str(self.file_num))
        print('[{}] Data frame loaded'.format(self.name))
        print('[{}] Encoding file {}...'.format(self.name, self.file_num))
        df.to_csv(file_path_new % str(self.file_num), sep=',', header=True)
        print('[{}] File #{} Encoded!'.format(self.name, self.file_num))


file_path = 'C:/Users/rajmu/Desktop/taxi-split/taxi-split-%s.csv'
file_path_new = 'C:/Users/rajmu/Desktop/taxi-split/corrected/taxi-split-%s.csv'

    # This method gets rid of empty rows from the dataset if there are any
def export_corrected(file_num, is_range=False):
    if is_range:
        bar = ShadyBar(message="Loading dataset",
                   suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta_td)s',
                   max=file_num * 2)
        threads = list()
        for file in range(1, file_num + 1):
            #export_single(file, bar)
            t = SplitThread(file, 'SplitThread-{}'.format(file), file)
            t.start()
            threads.append(t)
        for _t in threads:
            _t.join()
        print('Job complete. {} Threads executed'.format(file_num))
    else:
        bar = ShadyBar(message="Loading dataset",
                   suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta_td)s',
                   max=2)
        export_single(file_num, bar)


def export_single(file, bar):
        bar.message='Loading data frame #%d' % file
        bar.update()
        df = pd.read_csv(file_path % str(file))
        bar.next()
        bar.message = 'Encoding request #%d' % file
        bar.update()
        df.to_csv(file_path_new % str(file), sep=',', header=True)
        bar.next()


def main(argv):
    nums = int(argv[1])
    r = False
    if len(argv) > 2:
        if "range" in str(argv[2]):
            r = True
    export_corrected(nums, r)


if __name__ == "__main__":
    main(sys.argv)
