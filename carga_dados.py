import pandas as pd
import logging

class CargaDados:

    df_seg = []

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
    
    def executar(self):
        logging.info('Carregando dados de segmentos...')
        colunas = ['id_ato', 'data_pub', 'tipo_ato', 'id_seg', 'tipo_seg', 'txt_seg']
        self.df_seg = pd.read_csv('./datasets/extracao-segmentos-atos.csv', 
                            delimiter='|', names=colunas, quotechar="'")
        logging.info('{0} registros carregados.'.format(self.df_seg['id_seg'].count()))

        return self.df_seg