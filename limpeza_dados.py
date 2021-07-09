import pandas as pd
import logging
import re
from html.parser import HTMLParser

class LimpezaDados:

    df_seg = []

    def __init__(self, df_seg):
        logging.basicConfig(level=logging.INFO)
        self.df_seg = df_seg

    def remover_tags_html(self):
        logging.info('Removendo tags HTML...')
        padrao_tag_html = re.compile('<.*?>')
        remover_tags = lambda txt : re.sub(padrao_tag_html, '', str(txt)) 
        self.df_seg['txt_seg'] = self.df_seg['txt_seg'].apply(remover_tags)
    
    def executar(self):
        self.remover_tags_html()
        logging.info('Limpeza de dados concluída.')
        return self.df_seg