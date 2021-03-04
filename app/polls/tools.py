import glob
import os
import csv
from polls.models import TaxiService

def insert_db():
    BASE_DIR = 'C:\\Users\\ASUS\\Downloads\\Frogtek\\django_test\\datos\\datos\\'
    os.chdir(BASE_DIR)
    csv_files = glob.glob('*.{}'.format('csv'))
    list_data = []

    for filename in csv_files:
        with open(filename) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                date = row[1][7]

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

    #                 list_data.append(TaxiService(**data))
    #
    #         if len(list_data) == 10000:
    #             #TaxiService.objects.bulk_create(list_data)
    #             list_data = []
    #
    # if len(list_data) != 0:
    #     TaxiService.objects.bulk_create(list_data)


# def load_dataframe():
#     BASE_DIR = 'C:\\Users\\ASUS\\Downloads\\Frogtek\\django_test\\datos\\datos\\'
#     os.chdir(BASE_DIR)
#     csv_files = glob.glob('*.{}'.format('csv'))
#     list_data = []
#
#     for filename in csv_files:
#         data = pd.read_csv(filename)
#         list_data.append(data)
#
#     df = pd.concat(list_data, ignore_index=True)
#
#     df1 = df.loc[df['mes'] == '2020-01']
#     df2 = df.loc[df['mes'] == '2020-02']
#     df3 = df.loc[df['mes'] == '2020-03']
#     df = pd.concat([df1, df2, df3], ignore_index=True)
#
#     df = df.reset_index()
#     df = df.rename(columns={'index': 'id'})
#
#     df.id = pd.to_numeric(df.id, downcast='integer')
#     df.passenger_count = pd.to_numeric(df.passenger_count, downcast='integer')
#     df.PULocationID = pd.to_numeric(df.PULocationID, downcast='integer')
#     df.DOLocationID = pd.to_numeric(df.DOLocationID, downcast='integer')
#     df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
#     df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
#     # df['store_and_fwd_flag'] = df['store_and_fwd_flag'].astype(str)
#
#     return df

# def insert_db():
#     PATH = os.getcwd()
#     dataframe = load_dataframe()
#     os.chdir(PATH)
#
#     # print(dataframe.dtypes)
#     # print(dataframe)
#
#     database_username = 'root'
#     database_password = ''
#     database_ip = 'localhost'
#     database_name = 'app-db'
#
#     engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(database_username, database_password,
#                                                                             database_ip, database_name), echo=False)
#     #cnx = engine.raw_connection()
#     dataframe.to_sql(name='polls_taxiservice', con=engine, if_exists='replace', index=False)
#
#     with engine.begin() as conn:
#         conn.execute('SELECT * FROM polls_taxiservice')

insert_db()