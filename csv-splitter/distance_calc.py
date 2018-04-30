from datasets import CrimeRecord
from datasets import TaxiTrip
from tmanager import ThreadManager
from progress.bar import IncrementalBar
import csv

class Importer(object):


    def convert_header(csvheader, delimeter=','):
        cols = [x for x in str(csvheader).split(delimeter)]
        return cols


    def model_crime(self, header, row):
        id = row[header.index('ID')]
        date = row[header.index('Date')]
        commarea = row[header.index('Community Area')]
        latt = row[header.index('Latitude')]
        long = row[header.index('Longitude')]
        return CrimeRecord(id, date, commarea, latt, long)


    def model_taxi(self, header, row):
        pass


    def import_crime(self, path):
        if path == '' or path is None:
            raise ValueError('Invalid path!')
        with open(path) as file:
            print('loading csv...')
            reader = csv.reader(file)

            header = next(reader)
            data = [x for x in reader]
            row_count = len(data)
            print('Loading completed. {} lines'.format(row_count))
            crimes = list()
            bar_count = (int(row_count / 100) * 100) + 100
            bar = IncrementalBar('Modelling Crimes', max=bar_count, suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta_td)s')
            for index, row in enumerate(data):
                crimes.append(self.model_crime(header, row))
                if index % 100 == 0:
                    bar.next(100)
            print('\nimport finished')
            return crimes


    def import_taxi(self, path):
        if path == '' or path is None:
            raise ValueError('Invalid path!')
        with open(path) as file:
            print('loading csv...')
            reader = csv.reader(file)

            header = next(reader)
            data = [x for x in reader]
            row_count = len(data)
            print('Loading completed. {} lines'.format(row_count))
            taxis = list()
            bar_count = (int(row_count / 100) * 100) + 100
            bar = IncrementalBar('Modelling Taxi Trips', max=bar_count, suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta_td)s')
            for index, row in enumerate(data):
                taxis.append(self.model_taxi(header, row))
                if index % 100 == 0:
                    bar.next(100)
            print('\nimport finished')
            return taxis



importer = Importer()
path = 'C:/Users/rajmu/Desktop/project-4/crime_dataset.csv'
result = importer.import_crime(path)
print(result[0].id)
