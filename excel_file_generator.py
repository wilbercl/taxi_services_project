import pandas as pd
import glob
import os
import numpy as np


class ExcelGenerator():
    def write_excel(self, dataframe, writer, sheet_name):
        dataframe.to_excel(writer, index=False, sheet_name=sheet_name)

    def load_dataframe(self):
        BASE_DIR = os.getcwd() + "\datos\\"
        os.chdir(BASE_DIR)
        csv_files = glob.glob('*.{}'.format('csv'))
        list_data = []

        for filename in csv_files:
            data = pd.read_csv(filename)
            list_data.append(data)

        return pd.concat(list_data, ignore_index=True)

    def execute(self, dataframe, condition):
        dataframe_new = dataframe.loc[condition]

        groupby_df = dataframe_new.groupby(['mes', 'tipo_dia']).agg({'passenger_count': ['count', 'sum'],
                                                                      'trip_distance': ['count', 'sum']})

        groupby_df.columns = ['pt_c', 'personas_transportadas', 'total_servicios', 'millas_recorridas']
        groupby_df = groupby_df.reset_index()
        groupby_df = groupby_df.drop(['pt_c'], axis=1)
        groupby_df = groupby_df[['mes', 'tipo_dia', 'personas_transportadas', 'millas_recorridas', 'total_servicios']]

        return groupby_df

    def start(self):
        PATH = os.getcwd()
        dataframe = self.load_dataframe()

        #cambio el typo de objeto del campo "tpep_pickup_datetime" para tratarlo como una fecha
        dataframe.tpep_pickup_datetime = pd.to_datetime(dataframe.tpep_pickup_datetime)

        os.chdir(PATH)

        dataframe['mes'] = dataframe['tpep_pickup_datetime'].dt.strftime('%Y-%m')
        dataframe['tipo_dia'] = np.where(dataframe['tpep_pickup_datetime'].dt.dayofweek >= 5, '2', '1')

        #Elimino los registros que la fecha sea diferente a los meses de enero, febreo, marzo de 2020
        df1 = dataframe.loc[dataframe['mes'] == '2020-01']
        df2 = dataframe.loc[dataframe['mes'] == '2020-02']
        df3 = dataframe.loc[dataframe['mes'] == '2020-03']
        list = [df1, df2, df3]
        dataframe = pd.concat(list, ignore_index=True)

        #Elimino los registros donde la columna trip_distance <= 0
        dataframe = dataframe.drop(dataframe[dataframe['trip_distance'] <= 0].index)

        #Elimino los registros donde la columna fare_amount <= 0
        dataframe = dataframe.drop(dataframe[dataframe['fare_amount'] <= 0].index)

        ##Elimino los registros donde la columna tolls_amount < 0
        dataframe = dataframe.drop(dataframe[dataframe['tolls_amount'] < 0].index)

        # Elimino los registros donde la columna extra < 0
        dataframe = dataframe.drop(dataframe[dataframe['extra'] < 0].index)

        # Elimino los registros donde la columna mta_tax < 0
        dataframe = dataframe.drop(dataframe[dataframe['mta_tax'] < 0].index)

        groupby_jfk = self.execute(dataframe, lambda df: df['RatecodeID'] == 2)
        groupby_regular = self.execute(dataframe, lambda df: df['RatecodeID'] == 1)
        groupby_others = self.execute(dataframe, lambda df: (df['RatecodeID'] != 2) & (df['RatecodeID'] != 1))

        with pd.ExcelWriter("file.xlsx") as writer:
            self.write_excel(groupby_jfk, writer, "JFK")
            self.write_excel(groupby_regular, writer, "Regular")
            self.write_excel(groupby_others, writer, "Others")


if __name__ == '__main__':
    e_g = ExcelGenerator()
    e_g.start()