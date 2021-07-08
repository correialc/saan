import pandas as pd
import logging

class LimpezaDados:

    df_seg = []

    def __init__(self, df_seg):
        logging.basicConfig(level=logging.INFO)
        self.df_seg = df_seg
    
    def executar(self):
        logging.info('Etapa limpeza dados...')
        return self.df_seg