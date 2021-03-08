import glob
import numpy as np
import os
import pandas as pd


class ExcelGenerator():
    def __init__(self, base_dir, file_name='file.xlsx'):
        self.file_name = file_name
        self.base_dir = base_dir

    def load_dataframe(self):
        os.chdir(self.base_dir)
        csv_files = glob.glob('*csv')

        list_data = [pd.read_csv(filename) for filename in csv_files]

        return pd.concat(list_data, ignore_index=True)

    def execute_query(self, dataframe, condition):
        dataframe_new = dataframe.loc[condition]

        groupby_df = dataframe_new.groupby(['mes', 'tipo_dia']).agg({'passenger_count': ['count', 'sum'],
                                                                      'trip_distance': ['count', 'sum']})

        groupby_df.columns = ['pt_c', 'personas_transportadas', 'total_servicios', 'millas_recorridas']
        groupby_df = groupby_df.reset_index()
        groupby_df = groupby_df.drop(['pt_c'], axis=1)
        groupby_df = groupby_df[['mes', 'tipo_dia', 'personas_transportadas', 'millas_recorridas', 'total_servicios']]

        return groupby_df

    def data_cleaning(self, dataframe):
        # Elimino los registros que la fecha sea diferente a los meses de enero, febrero, marzo de 2020
        df1 = dataframe.loc[dataframe['mes'] == '2020-01']
        df2 = dataframe.loc[dataframe['mes'] == '2020-02']
        df3 = dataframe.loc[dataframe['mes'] == '2020-03']
        list = [df1, df2, df3]
        dataframe = pd.concat(list, ignore_index=True)

        # Elimino los registros donde la columna trip_distance <= 0
        dataframe = dataframe.drop(dataframe[dataframe['trip_distance'] <= 0].index)

        # Elimino los registros donde la columna fare_amount <= 0
        dataframe = dataframe.drop(dataframe[dataframe['fare_amount'] <= 0].index)

        ##Elimino los registros donde la columna tolls_amount < 0
        dataframe = dataframe.drop(dataframe[dataframe['tolls_amount'] < 0].index)

        # Elimino los registros donde la columna extra < 0
        dataframe = dataframe.drop(dataframe[dataframe['extra'] < 0].index)

        # Elimino los registros donde la columna mta_tax < 0
        dataframe = dataframe.drop(dataframe[dataframe['mta_tax'] < 0].index)

        return dataframe

    def generate_excel_file(self):
        path = os.getcwd()
        dataframe = self.load_dataframe()

        #cambio el tipo de objeto del campo "tpep_pickup_datetime" para tratarlo como una fecha
        dataframe.tpep_pickup_datetime = pd.to_datetime(dataframe.tpep_pickup_datetime)

        os.chdir(path)

        dataframe['mes'] = dataframe['tpep_pickup_datetime'].dt.strftime('%Y-%m')
        dataframe['tipo_dia'] = np.where(dataframe['tpep_pickup_datetime'].dt.dayofweek >= 5, '2', '1')

        dataframe = self.data_cleaning(dataframe)

        groupby_jfk = self.execute_query(dataframe, lambda df: df['RatecodeID'] == 2)
        groupby_regular = self.execute_query(dataframe, lambda df: df['RatecodeID'] == 1)
        groupby_others = self.execute_query(dataframe, lambda df: (df['RatecodeID'] != 2) & (df['RatecodeID'] != 1))

        with pd.ExcelWriter(self.file_name) as writer:
            groupby_jfk.to_excel(writer, index=False, sheet_name="JFK")
            groupby_regular.to_excel(writer, index=False, sheet_name="Regular")
            groupby_others.to_excel(writer, index=False, sheet_name="Others")


if __name__ == '__main__':
    dir_file = input('Ingrese la ruta absoluta donde se encuentren los archivos .csv: ')
    ExcelGenerator(dir_file).generate_excel_file()