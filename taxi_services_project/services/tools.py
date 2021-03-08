import csv
import decimal
import glob
import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taxi_services_project.settings")
django.setup()

from services.models import TaxiService


class LoadData():
    def insert_db(self, path):
        os.chdir(path)
        csv_files = glob.glob('*.csv')
        list_data = []

        for filename in csv_files:
            with open(filename) as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    date = row[1][:7]
                    trip_distance = decimal.Decimal(row[4])
                    fare_amount = decimal.Decimal(row[10])
                    extra = decimal.Decimal(row[11])
                    mta_tax = decimal.Decimal(row[12])
                    tolls_amount = decimal.Decimal(row[14])

                    amounts_non_zero = trip_distance > 0 and fare_amount > 0
                    positive_amount = extra >= 0 and mta_tax >= 0 and tolls_amount >= 0

                    if date in ['2020-01', '2020-02', '2020-03'] and amounts_non_zero and positive_amount:
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


if __name__ == '__main__':
    dir_file = input('Ingrese la ruta absoluta donde se encuentren los archivos .csv: ')
    LoadData().insert_db(dir_file)