from datasets import CrimeRecord
from datasets import TaxiTrip
from tmanager import ThreadManager
from progress.bar import IncrementalBar
import csv
import math
import datetime
import time

class ModelException(Exception):
    def __init__(self, message, errors=None):
        super(Exception, self).__init__(message)
        self.errors = errors

class Importer(object):


    def convert_header(csvheader, delimeter=','):
        cols = [x for x in str(csvheader).split(delimeter)]
        return cols


    def partition(self, iterable, chunk_size=1000):
        return [iterable[x:x+chunk_size] for x in range(0, len(iterable), chunk_size)]


    def model_crime(self, header, row):
        id = row[header.index('ID')]
        date = row[header.index('Date')]
        commarea = row[header.index('Community Area')]
        latt = row[header.index('Latitude')]
        long = row[header.index('Longitude')]
        try:
            if '.0' in commarea:
                commarea = commarea[:2]
            c = CrimeRecord(id, date, int(commarea), latt, long)
        except Exception as ex:
            raise ModelException(ex)
        return c


    def model_taxi(self, header, row):
        trip_id = row[header.index('Trip ID')]
        date = row[header.index('Trip Start Timestamp')]
        area = row[header.index('Pickup Community Area')]
        latt = row[header.index('Pickup Centroid Latitude')]
        long = row[header.index('Pickup Centroid Longitude')]
        try:
            t = TaxiTrip(trip_id, date, int(area), latt, long)
        except Exception as ex:
            raise ModelException(ex)
        return t


    def import_crime(self, path):
        if path == '' or path is None:
            raise ValueError('Invalid path!')
        with open(path) as file:
            print('loading crime csv... from {}'.format(path))
            reader = csv.reader(file)

            header = next(reader)
            data = list()#[x for x in reader]
            for x in reader:
                data.append(x)
            row_count = len(data)
            print('Loading completed. {} lines'.format(row_count))
            crimes = list()
            bar_count = (int(row_count / 1000) * 1000) + 1000
            bar = IncrementalBar('Modelling Crimes', max=bar_count, suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta_td)s')
            for index, row in enumerate(data):
                c = None
                try:
                    c = self.model_crime(header, row)
                except ModelException as me:
                    continue
                if c is not None:
                    crimes.append(c)
                if index % 1000 == 0:
                    bar.next(1000)
            print('\nimport finished')
            return crimes


    def import_taxi(self, path):
        if path == '' or path is None:
            raise ValueError('Invalid path!')
        with open(path) as file:
            print('loading taxi csv... from {}'.format(path))
            reader = csv.reader(file, delimiter=';', quotechar='"')

            head = next(reader)
            head[0] = 'Trip ID'
            header =list()
            for element in head:
                header.append(element.replace('`',' '))
            data = list()#[x for x in reader]
            for x in reader:
                data.append(x)
            row_count = len(data)
            print('Loading completed. {} lines'.format(row_count))
            taxis = list()
            bar_count = (int(row_count / 1000) * 1000) + 1000
            bar = IncrementalBar('Modelling Taxi Trips', max=bar_count, suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta_td)s')
            for index, row in enumerate(data):
                t = None
                try:
                    t = self.model_taxi(header, row)
                except ModelException as me:
                    continue
                if t is not None:
                    taxis.append(t)
                if index % 1000 == 0:
                    bar.next(1000)
            print('\nimport finished')
            return taxis



class Distance(object):

    neighbours = {1: [1,2,4,77],
                2: [2,1,13,14,77],
                3: [3,4,5,6,77],
                4: [4,2,3,5,13,14,16],
                5: [5,3,4,6,7,14,16,21,22],
                6: [6,3,4,5,7],
                7: [7,5,6,8,21,22,24],
                8: [8,7,22,24,28,32],
                9: [9,10,12,76],
                10: [10,9,11,12,15,17,76],
                11: [11,10,12,15],
                12: [12,10,11,13,14,15,16],
                13: [13,2,4,12,14],
                14: [14,4,5,12,13,15,16],
                15: [15,11,12,14,16,17,19,20],
                16: [16,4,5,11,12,14,15,20,21],
                17: [17,15,18,19,76],
                18: [18,17,19,25],
                19: [19,15,16,17,18,20,25],
                20: [20,15,16,19,21,22,23,25],
                21: [21,5,16,20,22],
                22: [22,5,7,20,21,23,24],
                23: [23,20,22,24,25,26,27,28],
                24: [24,7,8,22,23,27,28,32],
                25: [25,18,19,20,23,26],
                26: [26,23,25,27,29],
                27: [27,23,24,26,28,29],
                28: [28,8,23,24,27,29,30,31,32,33,34],
                29: [29,26,27,28,30,31],
                30: [30,28,29,31,56,57,58,59],
	            31: [31,28,29,30,33,34,58,59,60],
	            32: [32,8,28,33],
	            33: [33,28,31,32,34,35],
	            34: [34,28,31,33,35,37,38,61],
	            35: [35,33,34,36,37,38],
	            36: [36,35,38,39],
	            37: [37,34,35,38,40,60,61,68],
	            38: [38,34,35,36,37,39,40,41],
	            39: [39,36,38,40,41],
	            40: [40,37,38,39,41,42,68,69],
	            41: [41,38,39,40,42],
	            42: [42,40,41,43,69],
	            43: [43,42,45,46,69],
	            44: [44,45,47,49,50,71,73],
	            45: [45,43,44,46,47,48,69],
	            46: [46,43,45,48,51,52],
	            47: [47,44,45,48,49,50,51],
	            48: [48,44,45,46,47,50,51,52],
	            49: [49,44,47,50,53,54],
	            50: [50,44,47,48,49,51,53,54],
	            51: [51,46,47,48,50,52,54,55],
	            52: [52,46,48,51,55],
	            53: [53,49,50,54,75],
	            54: [54,49,50,51,53,55],
	            55: [55,51,52,54],
	            56: [56,30,57,62,64,65],
	            57: [57,30,56,58,62,63],
	            58: [58,30,31,57,59,61,62,63],
	            59: [59,30,31,58,60,61],
	            60: [60,31,34,37,59,61],
	            61: [61,37,58,59,60,63,66,67,68],
	            62: [62,56,57,58,63,64,65,66],
	            63: [63,57,58,61,62,65,66,67],
	            64: [64,56,62,65],
	            65: [65,56,62,63,64,66,70],
	            66: [66,62,63,65,67,70,71],
	            67: [67,61,63,66,68,70,71],
	            68: [68,37,40,61,67,69,71],
	            69: [69,40,42,43,44,45,71],
	            70: [70,65,66,67,71,72],
	            71: [71,44,49,66,67,68,69,70,72,73],
	            72: [72,70,71,73,74,75],
	            73: [73,44,49,71,72,75],
	            74: [74,72,75],
	            75: [75,49,53,72,73,74],
	            76: [76,9,10,17],
	            77: [77,1,2,3,4]}

    def __init__(self, start_days, stop_days):
        self.start_days = start_days #string timestamp 'h1', 'd3'
        self.stop_days = stop_days


    def MAX_DISTANCE(self):
        return float(1.5) #km


    def get_neighbours(self, community):
        return Distance.neighbours[community]


    @staticmethod
    def to_rad(deg):
        return deg * (math.pi/180)

    #calculates the distance between 2 objects
    def get_distance(self, crime, taxi):
        x1 = float(crime.point['x'])
        y1 = float(crime.point['y'])
        x2 = float(taxi.point['x'])
        y2 = float(taxi.point['y'])
        dx = Distance.to_rad(x2-x1)
        dy = Distance.to_rad(y2-y1)
        R = 6371
        a = math.sin(dx/2) * math.sin(dx/2) + math.cos(Distance.to_rad(y1)) * math.cos(Distance.to_rad(y2)) * math.sin(dy/2) * math.sin(dy/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        return d


    def get_taxis_per_crime(self, crime, taxi_list):
        taxi_l = list()

        #first narrow down taxi list to certain date period
        crime_time = datetime.datetime.strptime(crime.date, '%Y-%m-%d %H:%M:%S')

        #decoding time delta
        if 'd' in self.start_days:
            offset = int(self.start_days[1:])
            date_start = crime_time - datetime.timedelta(days=offset)
        elif 'h' in self.start_days:
            offset = int(self.start_days[1:])
            date_start = crime_time - datetime.timedelta(hours=offset)
        else:
            date_start = crime_time - datetime.timedelta(hours=1)
        
        if 'd' in self.stop_days:
            offset = int(self.stop_days[1:])
            date_end = crime_time + datetime.timedelta(days=offset)
        elif 'h' in self.stop_days:
            offset = int(self.stop_days[1:])
            date_end = crime_time + datetime.timedelta(hours=offset)
        else:
            date_end = crime_time + datetime.timedelta(hours=1)

        final_taxi = list()

        #iterate through a taxi list
        for taxi in taxi_list:
            stamp_truncated = taxi.tripStartTimestamp[:-4]
            taxi_date = datetime.datetime.strptime(stamp_truncated, '%Y-%m-%d %H:%M:%S')
            if taxi_date > date_start and taxi_date < date_end:
                neeeigh = Distance.neighbours[crime.community_area]
                if int(taxi.pickupCommunityArea) in neeeigh:
                    if self.get_distance(crime, taxi) < self.MAX_DISTANCE():
                        final_taxi.append(taxi.trip_id)

        return crime.id, final_taxi

    def __log__(self, message, thread=None):
        if thread is None:
            print('[{}] (CrimeDistCalc) {}'.format(str(datetime.datetime.now()), str(message)))
        else:
            print('[{}] (CrimeDistCalc) [Thread: {}] {}'.format(str(datetime.datetime.now()), str(thread), str(message)))


    def run(self, arguments):
        args = arguments['file']
        crime_list = args['crime_list']
        taxi_list = args['taxi_list']
        out_path = args['out_path']
        thread_name = arguments['thread']

        output_rows = list()
        current = int(time.time())

        output_rows.append('crime_id,taxi_id')
        for crime in crime_list:
            self.__log__('Analyzing crime [{}]'.format(crime.id), thread_name)
            k, v = self.get_taxis_per_crime(crime, taxi_list)
            self.__log__('Crime [{}] analyzed! {} taxi matches found!'.format(k, len(v)), thread_name)
            if len(v) > 0:
                for taxi_id in v:
                    output_rows.append('{},{}'.format(k, taxi_id))

        with open(out_path.format('{}-{}'.format(current, thread_name)), 'w') as out_file:
            self.__log__('Opening file... {}'.format(out_path.format('{}-{}'.format(current, thread_name))))
            out_file.writelines(output_rows)
            
        self.__log__('Operation finished for thread {}'.format(thread_name))



