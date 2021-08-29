import pandas as pd
import logging

class CargaDados:

    path_dados_seg=None
    cabecalho_dados_seg=None

    def __init__(self, path_dados_seg='./dados/extracao-segmentos-atos.csv',
                    cabecalho_dados_seg=['id_ato', 'data_pub', 'tipo_ato', 
                                        'id_seg', 'tipo_seg', 'txt_seg']):
        
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt='%H:%M:%S')
        self.path_dados_seg = path_dados_seg
        self.cabecalho_dados_seg = cabecalho_dados_seg
    
    def executar(self, dados):
        logging.info('Carregando dados de segmentos...')
        dados.orig = pd.read_csv(self.path_dados_seg, delimiter='|', 
                                    names=self.cabecalho_dados_seg, quotechar="'")
        logging.info('{0} registros carregados.'.format(dados.orig['id_seg'].count()))
