import pandas as pd
import datetime as dt


class DateSorter:
    #This part MIGHT be fked as we dont know how the args are passed but the logic is kinda json-y and self explanatory
    def split(self, args):
        if args['file'] != "":
            path = args['file']
        else:
            pass
        df = pd.read_csv(path, sep=",")

        df['Pickup Centroid Location'] = df['Pickup Centroid Location'].astype(str)
        df['Dropoff Centroid  Location'] = df['Dropoff Centroid  Location'].astype(str)
        df = df[df['Pickup Centroid Location'] != 'nan']
        df = df[df['Dropoff Centroid  Location'] != 'nan']
        df['Trip Start Timestamp'] = df['Trip Start Timestamp'].apply(lambda x: dt.datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p'))
        df['Trip End Timestamp'] = df['Trip End Timestamp'].apply(lambda y: dt.datetime.strptime(y, '%m/%d/%Y %I:%M:%S %p'))

        df['Trip Start Timestamp'] = df['Trip Start Timestamp'].apply(lambda a: dt.datetime.strftime(a, '%d/%m/%Y %I:%M:%S %p'))
        df['Trip End Timestamp'] = df['Trip End Timestamp'].apply(lambda b: dt.datetime.strftime(b, '%d/%m/%Y %I:%M:%S %p'))

        df['Trip Start Timestamp'] = pd.to_datetime(df['Trip Start Timestamp'])
        df['Trip End Timestamp'] = pd.to_datetime(df['Trip End Timestamp'])

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
        #!!!!!!!!!!!!!!!!!!!!!!!!!!
        #args['file'] = JUST THE FILENAME, NOT ENTIRE PATH, FIX THIS WHEN WE KNOW EVERYTHING WORKS, CAN BE EXCHANGED TO PATH VARIABLE

        _2013firstQuarter.to_csv("2013firstQuarter" + args['file'] + '.csv', index=False)
        _2013secondQuarter.to_csv("2013secondQuarter" + args['file'] + '.csv', index=False)
        _2013thirdQuarter.to_csv("2013thirdQuarter" + args['file'] + '.csv', index=False)
        _2013fourthQuarter.to_csv("2013fourthQuarter" + args['file'] + '.csv', index=False)

        _2014firstQuarter.to_csv("2014firstQuarter" + args['file'] + '.csv', index=False)
        _2014secondQuarter.to_csv("2014secondQuarter" + args['file'] + '.csv', index=False)
        _2014thirdQuarter.to_csv("2014thirdQuarter" + args['file'] + '.csv', index=False)
        _2014fourthQuarter.to_csv("2014fourthQuarter" + args['file'] + '.csv', index=False)

        _2015firstQuarter.to_csv("2015firstQuarter" + args['file'] + '.csv', index=False)
        _2015secondQuarter.to_csv("2015secondQuarter" + args['file'] + '.csv', index=False)
        _2015thirdQuarter.to_csv("2015thirdQuarter" + args['file'] + '.csv', index=False)
        _2015fourthQuarter.to_csv("2015fourthQuarter" + args['file'] + '.csv', index=False)

        _2016firstQuarter.to_csv("2016firstQuarter" + args['file'] + '.csv', index=False)
        _2016secondQuarter.to_csv("2016secondQuarter" + args['file'] + '.csv', index=False)
        _2016thirdQuarter.to_csv("2016thirdQuarter" + args['file'] + '.csv', index=False)
        _2016fourthQuarter.to_csv("2016fourthQuarter" + args['file'] + '.csv', index=False)

        _2017firstQuarter.to_csv("_2017firstQuarter" + args['file'] + '.csv', index=False)
        _2017secondQuarter.to_csv("_2017secondQuarter" + args['file'] + '.csv', index=False)
        _2017thirdQuarter.to_csv("_2017thirdQuarter" + args['file'] + '.csv', index=False)
        _2017fourthQuarter.to_csv("_2017fourthQuarter" + args['file'] + '.csv', index=False)



