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
    
    def remover_segmentos_nao_representativos(self):
        logging.info('Removendo segmentos não representativos...')
        tipos_seg_representativos = ['Artigo', 'Não Identificado', 'Ementa', 'Fecho', 'Inciso']
        qtd_seg = self.df_seg['id_seg'].count()
        qtd_seg_rep = self.df_seg['tipo_seg'].isin(tipos_seg_representativos).sum()
        self.df_seg = self.df_seg[self.df_seg['tipo_seg'].isin(tipos_seg_representativos)]
        logging.info(f'{qtd_seg - qtd_seg_rep} segmentos não representativos excluídos.')
        logging.info(f'Restaram {qtd_seg_rep} segmentos representativos.')

    def remover_segmentos_nulos(self):
        logging.info('Removendo segmentos nulos...')
        qtd_seg = self.df_seg['id_seg'].count()
        qtd_seg_na = self.df_seg['txt_seg'].isna().sum()
        self.df_seg = self.df_seg[self.df_seg['txt_seg'].notna()]
        logging.info(f'{qtd_seg_na} segmentos nulos excluídos.')
        logging.info(f'Restaram {qtd_seg - qtd_seg_na} segmentos não nulos.')

    def remover_tags_html(self):
        logging.info('Removendo tags HTML...')
        padrao_tag_html = re.compile('<.*?>')
        remover_tags = lambda txt : re.sub(padrao_tag_html, '', str(txt)) 
        self.df_seg['txt_seg'] = self.df_seg['txt_seg'].apply(remover_tags)
    
    def remover_escape_html(self):
        logging.info('Removendo caracteres de escape HTML...')
        remover_escape_chars = lambda txt : HTMLParser().unescape(txt)
        self.df_seg['txt_seg'] = self.df_seg['txt_seg'].apply(remover_escape_chars)

    def reclassificar_nao_identificados(self):
        logging.info('Reclassificando segmentos não identificados...')
        df_seg_ni = self.df_seg[self.df_seg['tipo_seg'] == 'Não Identificado']
        padrao_artigo = re.compile('^\s{0,}Art[\s\.]')
        qtd_seg_reclassificaveis = df_seg_ni[df_seg_ni['txt_seg'].str.contains(padrao_artigo)].count()['id_seg']
        ids_reclassificaveis = df_seg_ni[df_seg_ni['txt_seg'].str.contains(padrao_artigo)]['id_seg']
        self.df_seg.loc[self.df_seg['id_seg'].isin(ids_reclassificaveis), 'tipo_seg'] = 'Artigo'
        logging.info(f'{qtd_seg_reclassificaveis} segmentos reclassificados como artigos.')

    def executar(self):
        self.remover_segmentos_nao_ade()
        self.remover_segmentos_nao_representativos()
        self.remover_segmentos_nulos()
        self.remover_tags_html()
        self.remover_escape_html()
        self.reclassificar_nao_identificados()
        logging.info('Limpeza de dados concluída.')
        return self.df_seg