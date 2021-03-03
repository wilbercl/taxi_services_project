import pandas as pd
import glob
import os
from sqlalchemy import create_engine

def load_dataframe():
    BASE_DIR = 'C:\\Users\\ASUS\\Downloads\\Frogtek\\django_test\\datos\\datos\\'
    os.chdir(BASE_DIR)
    csv_files = glob.glob('*.{}'.format('csv'))
    list_data = []

    for filename in csv_files:
        data = pd.read_csv(filename)
        list_data.append(data)

    df = pd.concat(list_data, ignore_index=True)
    df = df.reset_index()
    df = df.rename(columns={'index': 'id'})

    df.id = pd.to_numeric(df.id, downcast='integer')
    df.passenger_count = pd.to_numeric(df.passenger_count, downcast='integer')
    df.PULocationID = pd.to_numeric(df.PULocationID, downcast='integer')
    df.DOLocationID = pd.to_numeric(df.DOLocationID, downcast='integer')
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    # df['store_and_fwd_flag'] = df['store_and_fwd_flag'].astype(str)

    return df

def insert_db():
    PATH = os.getcwd()
    dataframe = load_dataframe()
    os.chdir(PATH)

    # print(dataframe.dtypes)
    # print(dataframe)

    database_username = 'root'
    database_password = ''
    database_ip = 'localhost'
    database_name = 'app-db'

    engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(database_username, database_password,
                                                                            database_ip, database_name), echo=False)
    #cnx = engine.raw_connection()
    dataframe.to_sql(name='polls_taxiservice', con=engine, if_exists='replace', index=False)

    with engine.begin() as conn:
        conn.execute('SELECT * FROM polls_taxiservice')

insert_db()