import pandas as pd
import logging
import re
from html.parser import HTMLParser

class LimpezaDados:

    df_seg = []

    def __init__(self, df_seg):
        logging.basicConfig(level=logging.INFO)
        self.df_seg = df_seg

    def remover_segmentos_nao_ade(self):
        logging.info('Excluindo segmentos dos atos que não são ADE...')
        qtd_seg = self.df_seg['id_seg'].count()
        self.df_seg = self.df_seg[self.df_seg['tipo_ato']=='ADE'].copy()
        qtd_seg_ade = self.df_seg['id_seg'].count()
        logging.info(f'{qtd_seg - qtd_seg_ade} segmentos de atos não ADE excluídos.')
        logging.info(f'Restaram {qtd_seg_ade} segmentos de atos ADE.')
    
    def remover_tags_html(self):
        logging.info('Removendo tags HTML...')
        padrao_tag_html = re.compile('<.*?>')
        remover_tags = lambda txt : re.sub(padrao_tag_html, '', str(txt)) 
        self.df_seg['txt_seg'] = self.df_seg['txt_seg'].apply(remover_tags)
    
    def remover_escape_html(self):
        logging.info('Removendo caracteres de escape HTML...')
        remover_escape_chars = lambda txt : HTMLParser().unescape(txt)
        self.df_seg['txt_seg'] = self.df_seg['txt_seg'].apply(remover_escape_chars)

    def executar(self):
        self.remover_segmentos_nao_ade()
        self.remover_tags_html()
        self.remover_escape_html()
        logging.info('Limpeza de dados concluída.')
        return self.df_seg