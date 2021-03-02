import pandas as pd
import glob
import os
import numpy as np

def write_excel(dataframe, writer, sheet_name):
    dataframe.to_excel(writer, index=False, sheet_name=sheet_name)

def load_dataframe():
    BASE_DIR = os.getcwd() + "\datos\datos\\"
    os.chdir(BASE_DIR)
    csv_files = glob.glob('*.{}'.format('csv'))
    list_data = []

    for filename in csv_files:
        data = pd.read_csv(filename)
        list_data.append(data)

    return pd.concat(list_data, ignore_index=True)

def execute(dataframe, condition):
    dataframe_new = dataframe.loc[condition]

    groupby_df = dataframe_new.groupby(['mes', 'tipo_dia']).agg({'passenger_count': ['count', 'sum'],
                                                                  'trip_distance': ['count', 'sum']})

    groupby_df.columns = ['pt_c', 'personas_transportadas', 'total_servicios', 'millas_recorridas']
    groupby_df = groupby_df.reset_index()
    groupby_df = groupby_df.drop(['pt_c'], axis=1)
    groupby_df = groupby_df[['mes', 'tipo_dia', 'personas_transportadas', 'millas_recorridas', 'total_servicios']]

    return groupby_df

def start():
    PATH = os.getcwd()
    dataframe = load_dataframe()

    #cambio el typo de objeto del campo "tpep_pickup_datetime" para tratarlo como una fecha
    dataframe.tpep_pickup_datetime = pd.to_datetime(dataframe.tpep_pickup_datetime)

    os.chdir(PATH)
    #print(dataframe.dtypes)

    dataframe['mes'] = dataframe['tpep_pickup_datetime'].dt.strftime('%Y-%m')
    dataframe['tipo_dia'] = np.where(dataframe['tpep_pickup_datetime'].dt.dayofweek >= 5, '2', '1')

    groupby_jfk = execute(dataframe, lambda df: df['RatecodeID'] == 2)
    groupby_regular = execute(dataframe, lambda df: df['RatecodeID'] == 1)
    groupby_others = execute(dataframe, lambda df: (df['RatecodeID'] != 2) & (df['RatecodeID'] != 1))

    with pd.ExcelWriter("test.xlsx") as writer:
        write_excel(groupby_jfk, writer, "JFK")
        write_excel(groupby_regular, writer, "Regular")
        write_excel(groupby_others, writer, "Others")

if __name__ == '__main__':
    start()