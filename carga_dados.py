import pandas as pd
import logging

class CargaDados:

    dados_seg = []
    path_dados_seg=None
    cabecalho_dados_seg=None

    def __init__(self, path_dados_seg='./extracao-segmentos-atos.csv',
                    cabecalho_dados_seg=['id_ato', 'data_pub', 'tipo_ato', 
                                        'id_seg', 'tipo_seg', 'txt_seg']):
        logging.basicConfig(level=logging.INFO)
        self.path_dados_seg = path_dados_seg
        self.cabecalho_dados_seg = cabecalho_dados_seg
    
    def executar(self):
        logging.info('Carregando dados de segmentos...')
        self.df_seg = pd.read_csv(self.path_dados_seg, delimiter='|', 
                                    names=self.cabecalho_dados_seg, quotechar="'")
        logging.info('{0} registros carregados.'.format(self.df_seg['id_seg'].count()))

        return self.df_seg