import glob
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from polls.models import TaxiService
import csv


def insert_db(path):

    os.chdir(path)
    csv_files = glob.glob('*.{}'.format('csv'))
    list_data = []

    for filename in csv_files:
        with open(filename) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                date = row[1][:7]

                if date == '2020-01' or date == '2020-02' or date == '2020-03':
                    data = {
                     'vendor_id': row[0],
                     'tpep_pickup_datetime': row[1],
                     'tpep_dropoff_datetime': row[2],
                     'passenger_count': row[3],
                     'trip_distance': row[4],
                     'rate_code_id': row[5],
                     'store_and_fwd_flag': row[6],
                     'pu_location_id': row[7],
                     'do_location_id': row[8],
                     'payment_type': row[9],
                     'fare_amount': row[10],
                     'extra': row[11],
                     'mta_tax': row[12],
                     'tip_amount': row[13],
                     'tolls_amount': row[14],
                     'improvement_surcharge': row[15],
                     'total_amount': row[16],
                     'congestion_surcharge': row[17]
                    }

                    list_data.append(TaxiService(**data))

            if len(list_data) == 10000:
                TaxiService.objects.bulk_create(list_data)
                list_data = []

    if len(list_data) != 0:
        TaxiService.objects.bulk_create(list_data)


insert_db('C:\\Users\\ASUS\\Downloads\\Frogtek\\django_test\\datos\\datos\\')

#insert_db('C:\\Users\\ASUS\\Downloads\\Frogtek\\django_test\\datos\\datos\\')