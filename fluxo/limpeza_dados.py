import pandas as pd
import logging
import re
from html.parser import HTMLParser

class LimpezaDados:

    def __init__(self, dados):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt='%H:%M:%S')
        dados.limp = dados.orig.copy()

    def remover_segmentos_nao_ade(self, dados):
        logging.info('Excluindo segmentos dos atos que não são ADE...')
        qtd_seg = dados.limp['id_seg'].count()
        dados.limp = dados.limp[dados.limp['tipo_ato']=='ADE'].copy()
        qtd_seg_ade = dados.limp['id_seg'].count()
        logging.info(f'{qtd_seg - qtd_seg_ade} segmentos de atos não ADE excluídos.')
        logging.info(f'Restaram {qtd_seg_ade} segmentos de atos ADE.')
        
    
    def remover_segmentos_nao_representativos(self, dados):
        logging.info('Removendo segmentos não representativos...')
        tipos_seg_representativos = ['Artigo', 'Não Identificado', 'Ementa', 'Fecho', 'Inciso']
        qtd_seg = dados.limp['id_seg'].count()
        qtd_seg_rep = dados.limp['tipo_seg'].isin(tipos_seg_representativos).sum()
        dados.limp = dados.limp[dados.limp['tipo_seg'].isin(tipos_seg_representativos)]
        logging.info(f'{qtd_seg - qtd_seg_rep} segmentos não representativos excluídos.')
        logging.info(f'Restaram {qtd_seg_rep} segmentos representativos.')
        

    def remover_segmentos_nulos(self, dados):
        logging.info('Removendo segmentos nulos...')
        qtd_seg = dados.limp['id_seg'].count()
        qtd_seg_na = dados.limp['txt_seg'].isna().sum()
        dados.limp = dados.limp[dados.limp['txt_seg'].notna()]
        logging.info(f'{qtd_seg_na} segmentos nulos excluídos.')
        logging.info(f'Restaram {qtd_seg - qtd_seg_na} segmentos não nulos.')
        

    def remover_tags_html(self, dados):
        logging.info('Removendo tags HTML...')
        padrao_tag_html = re.compile('<.*?>')
        remover_tags = lambda txt : re.sub(padrao_tag_html, '', str(txt)) 
        dados.limp['txt_seg'] = dados.limp['txt_seg'].apply(remover_tags)
        
    
    def remover_escape_html(self, dados):
        logging.info('Removendo caracteres de escape HTML...')
        remover_escape_chars = lambda txt : HTMLParser().unescape(txt)
        dados.limp['txt_seg'] = dados.limp['txt_seg'].apply(remover_escape_chars)
        

    def reclassificar_nao_identificados(self, dados):
        logging.info('Reclassificando segmentos não identificados...')
        seg_ni = dados.limp[dados.limp['tipo_seg'] == 'Não Identificado']
        padrao_artigo = re.compile('^\s{0,}Art[\s\.]')
        qtd_seg_reclassificaveis = seg_ni[seg_ni['txt_seg'].str.contains(padrao_artigo)].count()['id_seg']
        ids_reclassificaveis = seg_ni[seg_ni['txt_seg'].str.contains(padrao_artigo)]['id_seg']
        dados.limp.loc[dados.limp['id_seg'].isin(ids_reclassificaveis), 'tipo_seg'] = 'Artigo'
        logging.info(f'{qtd_seg_reclassificaveis} segmentos reclassificados como artigos.')
        

    def executar(self, dados):
        self.remover_segmentos_nao_ade(dados)
        self.remover_segmentos_nao_representativos(dados)
        self.remover_segmentos_nulos(dados)
        self.remover_tags_html(dados)
        self.remover_escape_html(dados)
        #self.reclassificar_nao_identificados(dados)
        logging.info('Limpeza de dados concluída.')