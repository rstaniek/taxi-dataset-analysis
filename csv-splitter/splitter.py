from progress.bar import IncrementalBar
import os
#from csv import reader

def split(filehandler, delimiter=',', row_limit=1000,
          output_name_template='output_%s.csv', output_path='.', keep_headers=True):
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = next(reader)
        current_out_writer.writerow(headers)
    bar = IncrementalBar('Splitting', max=113000000, suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta_td)s')
    for i, row in enumerate(reader):
        bar.next()
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)

#split the mo'fucker
split(open('C:/Users/rajmu/Desktop/Taxi_Trips.csv'), row_limit=1000000, output_name_template='taxi-split-%s.csv', output_path='C:/Users/rajmu/Desktop/taxi-split')
