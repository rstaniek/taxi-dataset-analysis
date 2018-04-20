import pandas as pd
import datetime as dt
from datetime import datetime
import time


class DateSorter:
    def __log__(self, message):
        print('[{}] (Sorter) {}'.format(str(datetime.now()), str(message)))


    def split(self, args):
        if args['file'] != "":
            path = args['file']
        else:
            pass
        if args['thread'] != "":
            thread_name = args['thread']

        self.__log__('Loading data frame {} on {}'.format(path, thread_name))
        df = pd.read_csv(path, sep=",")
        out_path = '%s-{}.csv' % path[:path.find('.')]
        out_path ='{}/by_quarter/{}'.format(out_path[:out_path.rfind('/')], out_path[out_path.rfind('/') + 1:])
        self.__log__('Data frame loaded. [{}]'.format(thread_name))

        self.__log__('Deleting rows without location data... [{}]'.format(thread_name))
        df['Pickup Centroid Location'] = df['Pickup Centroid Location'].astype(str)
        df['Dropoff Centroid  Location'] = df['Dropoff Centroid  Location'].astype(str)
        df = df[df['Pickup Centroid Location'] != 'nan']
        df = df[df['Dropoff Centroid  Location'] != 'nan']
        self.__log__('Non location data deleted. [{}]'.format(thread_name))

        self.__log__('Reformating date formats... [{}]'.format(thread_name))
        start_time = time.time()
        #df['Trip Start Timestamp'] = df['Trip Start Timestamp'].apply(lambda x: dt.datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p'))
        #df['Trip End Timestamp'] = df['Trip End Timestamp'].apply(lambda y: dt.datetime.strptime(y, '%m/%d/%Y %I:%M:%S %p'))

        #df['Trip Start Timestamp'] = df['Trip Start Timestamp'].apply(lambda a: dt.datetime.strftime(a, '%d/%m/%Y %I:%M:%S %p'))
        #df['Trip End Timestamp'] = df['Trip End Timestamp'].apply(lambda b: dt.datetime.strftime(b, '%d/%m/%Y %I:%M:%S %p'))

        df['Trip Start Timestamp'] = pd.to_datetime(df['Trip Start Timestamp'], format = '%m/%d/%Y %I:%M:%S %p', dayfirst=True)
        df['Trip End Timestamp'] = pd.to_datetime(df['Trip End Timestamp'], format = '%m/%d/%Y %I:%M:%S %p', dayfirst=True)
        elapsed_time = time.time() - start_time
        time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        self.__log__('Dates reformatted. Time elapsed: {} [{}]'.format(time_str, thread_name))

        self.__log__('Preparing to save output... [{}]'.format(thread_name))
        df.sort_values(by=['Trip Start Timestamp'], inplace=True)
        df['Quarter'] = df['Trip Start Timestamp'].dt.quarter
        df['Year'] = df['Trip Start Timestamp'].dt.year

        _2013firstQuarter = df[(df['Quarter'] == 1) & (df['Year'] == 2013)]
        _2013secondQuarter = df[(df['Quarter'] == 2) & (df['Year'] == 2013)]
        _2013thirdQuarter = df[(df['Quarter'] == 3) & (df['Year'] == 2013)]
        _2013fourthQuarter = df[(df['Quarter'] == 4) & (df['Year'] == 2013)]

        _2014firstQuarter = df[(df['Quarter'] == 1) & (df['Year'] == 2014)]
        _2014secondQuarter = df[(df['Quarter'] == 2) & (df['Year'] == 2014)]
        _2014thirdQuarter = df[(df['Quarter'] == 3) & (df['Year'] == 2014)]
        _2014fourthQuarter = df[(df['Quarter'] == 4) & (df['Year'] == 2014)]

        _2015firstQuarter = df[(df['Quarter'] == 1) & (df['Year'] == 2015)]
        _2015secondQuarter = df[(df['Quarter'] == 2) & (df['Year'] == 2015)]
        _2015thirdQuarter = df[(df['Quarter'] == 3) & (df['Year'] == 2015)]
        _2015fourthQuarter = df[(df['Quarter'] == 4) & (df['Year'] == 2015)]

        _2016firstQuarter = df[(df['Quarter'] == 1) & (df['Year'] == 2016)]
        _2016secondQuarter = df[(df['Quarter'] == 2) & (df['Year'] == 2016)]
        _2016thirdQuarter = df[(df['Quarter'] == 3) & (df['Year'] == 2016)]
        _2016fourthQuarter = df[(df['Quarter'] == 4) & (df['Year'] == 2016)]

        _2017firstQuarter = df[(df['Quarter'] == 1) & (df['Year'] == 2017)]
        _2017secondQuarter = df[(df['Quarter'] == 2) & (df['Year'] == 2017)]
        _2017thirdQuarter = df[(df['Quarter'] == 3) & (df['Year'] == 2017)]
        _2017fourthQuarter = df[(df['Quarter'] == 4) & (df['Year'] == 2017)]

        #Output to files

        self.__log__('Saving data to template: {} [{}]'.format(out_path, thread_name))
        _2013firstQuarter.to_csv(out_path.format('2013Q1'), index=False)
        _2013secondQuarter.to_csv(out_path.format('2013Q2'), index=False)
        _2013thirdQuarter.to_csv(out_path.format("2013Q3"), index=False)
        _2013fourthQuarter.to_csv(out_path.format("2013Q4"), index=False)

        _2014firstQuarter.to_csv(out_path.format("2014Q1"), index=False)
        _2014secondQuarter.to_csv(out_path.format("2014Q2"), index=False)
        _2014thirdQuarter.to_csv(out_path.format("2014Q3"), index=False)
        _2014fourthQuarter.to_csv(out_path.format("2014Q4"), index=False)

        _2015firstQuarter.to_csv(out_path.format("2015Q1"), index=False)
        _2015secondQuarter.to_csv(out_path.format("2015Q2"), index=False)
        _2015thirdQuarter.to_csv(out_path.format("2015Q3"), index=False)
        _2015fourthQuarter.to_csv(out_path.format("2015Q4"), index=False)

        _2016firstQuarter.to_csv(out_path.format("2016Q1"), index=False)
        _2016secondQuarter.to_csv(out_path.format("2016Q2"), index=False)
        _2016thirdQuarter.to_csv(out_path.format("2016Q3"), index=False)
        _2016fourthQuarter.to_csv(out_path.format("2016Q4"), index=False)

        _2017firstQuarter.to_csv(out_path.format("2017Q1"), index=False)
        _2017secondQuarter.to_csv(out_path.format("2017Q2"), index=False)
        _2017thirdQuarter.to_csv(out_path.format("2017Q3"), index=False)
        _2017fourthQuarter.to_csv(out_path.format("2017Q4"), index=False)
        self.__log__('Data saved! [{}]'.format(thread_name))



