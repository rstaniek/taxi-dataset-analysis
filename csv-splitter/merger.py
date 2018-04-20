# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:28:11 2018
@author: RedJohn
"""
import pandas as pd
import glob
import datetime as dt
from datetime import datetime
import time
import numpy as np


class ReMerger:
    
    def __log__(self, message):
        print('[{}] (ReMerger) {}'.format(str(datetime.now()), str(message)))
    
    def merger(self, args):
        
        if args['thread'] != "":
            thread_name = args['thread']
        else:
            pass
        path = args['file']
        
        #Folder will probably have to be changed to the one that holds the 1920 files
        files = glob.glob(path)
        #year = args['year']
        #quarter = args['quarter']
        it = args['iterable']
        year = int(it[:it.find('-')])
        quarter = int(it[it.find('-') + 1:])

        out_path = '%s-{}.csv' % path[:path.find('.')]
        out_path ='{}/merged/{}'.format(out_path[:out_path.rfind('/')], out_path[out_path.rfind('/') + 1:])
        
        #Creation of the dataframe that's going to hold the final data
        df = pd.DataFrame()
        
        self.__log__('Starting appending dataframes... [{}]'.format(thread_name))
        start_time = time.time()
        
        #Finding and appending files that match the required year and quarter
        for file in files:
            self.__log__('Loading data frame {} on {}'.format(file, thread_name))
            if str(str(year)+"Q"+str(quarter)) in file:
                auxiliaryFile = pd.read_csv(file, sep = ",")
                df = df.append(auxiliaryFile)
            self.__log__('Appended data frame {} on {}'.format(file, thread_name))
                
        elapsed_time = time.time() - start_time
        time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        self.__log__('Dates appended. Time elapsed: {} [{}]'.format(time_str, thread_name))

        df = df[df['Trip Start Timestamp'] is not np.NaN]
        
        
        #Sorting of dataframe by ¨Trip Start Timestamp¨
        self.__log__('Starting sorting the final dataframe... [{}]'.format(thread_name))
        start_time = time.time()
        
        df.sort_values(by=['Trip Start Timestamp'], inplace=True)
        
        elapsed_time = time.time() - start_time
        time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        self.__log__('Completed sorting. Time elapsed: {} [{}]'.format(time_str, thread_name))
        
        #Deletion of first column, auto generated index
        del df[0]
        
        #Saving of the output final quarter&year file
        df.to_csv(str(out_path.format("Final" + str(year) + "Q" + str(quarter))), index = False)
        self.__log__('Data saved! [{}]'.format(thread_name))
