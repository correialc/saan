import pandas as pd
import logging
import re
from html.parser import HTMLParser

class LimpezaDados:

    tipos_seg_por_tipo_ato = {
        'ADE': ['Artigo', 'Ementa', 'Fecho', 'Inciso', 'Não Identificado'],
        'Port.': ['Alínea', 'Artigo', 'Ementa', 'Fecho', 'Inciso', 'Não Identificado', 'Parágrafo'],
        'SC': ['Ementa', 'Fecho', 'Não Identificado']
    }


    def __init__(self, dados):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt='%H:%M:%S')

    def carregar_dados_originais(self, dados):
        logging.info('(Re)Carregando segmentos originais...')
        dados.limp = dados.orig.copy()

    def remover_segmentos_tipo_anexo(self, dados):
        logging.info('Removendo todos os segmentos do tipo Anexo...')
        qtd_seg_anexo = dados.limp[dados.limp['tipo_seg']=='Anexo']['id_seg'].count()
        dados.limp = dados.limp[dados.limp['tipo_seg']!='Anexo'].copy()
        logging.info(f'{qtd_seg_anexo} segmentos do tipo Anexo excluídos.')

    def remover_segmentos_filtro_tipo_ato(self, dados, tipo_ato):
        logging.info(f'Excluindo segmentos dos atos que não são {tipo_ato}...')
        qtd_seg = dados.limp['id_seg'].count()
        dados.limp = dados.limp[dados.limp['tipo_ato']==tipo_ato].copy()
        qtd_seg_filtrados = dados.limp['id_seg'].count()
        logging.info(f'{qtd_seg - qtd_seg_filtrados} segmentos de atos não {tipo_ato} excluídos.')
        logging.info(f'Restaram {qtd_seg_filtrados} segmentos de atos {tipo_ato}.')
        
    
    def remover_segmentos_nao_representativos(self, dados, tipo_ato):
        logging.info(f'Removendo segmentos não representativos para o tipo {tipo_ato}...')
        tipos_seg_representativos = self.tipos_seg_por_tipo_ato[tipo_ato]
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
        

    def executar(self, dados, tipo_ato):
        self.carregar_dados_originais(dados)
        self.remover_segmentos_nulos(dados)
        self.remover_segmentos_tipo_anexo(dados)
        self.remover_segmentos_filtro_tipo_ato(dados, tipo_ato)
        self.remover_segmentos_nao_representativos(dados, tipo_ato)
        self.remover_tags_html(dados)
        self.remover_escape_html(dados)
        #self.reclassificar_nao_identificados(dados)
        logging.info('Limpeza de dados concluída.')