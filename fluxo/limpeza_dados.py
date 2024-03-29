import pandas as pd
import logging
import re
import html

class LimpezaDados:

    tipos_seg_por_tipo_ato = {
        'ADE': ['Artigo', 'Ementa', 'Fecho', 'Inciso', 'Não Identificado'],
        'Port.': ['Alínea', 'Artigo', 'Ementa', 'Fecho', 'Inciso', 'Não Identificado', 'Parágrafo'],
        'SC': ['Ementa', 'Fecho', 'Não Identificado']
    }

    tipos_seg_padrao_regex = ['Artigo', 'Parágrafo', 'Alínea', 'Inciso']

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt='%H:%M:%S')


    def carregar_dados_originais(self, dados):
        logging.info('(Re)Carregando segmentos originais...')
        dados.limp = dados.orig.copy()


    def determinar_tipos_segmento(self, dados, tipo_ato):
        logging.info(f'Determinando tipos de segmento (labels) para atos do tipo {tipo_ato}...')
        dados.labels = list(filter(lambda lb : lb not in self.tipos_seg_padrao_regex, 
                                    self.tipos_seg_por_tipo_ato[tipo_ato]))
        logging.info(f'Tipos de segmento para atos {tipo_ato}: {dados.labels}')


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


    def remover_segmentos_padrao_regex(self, dados):
        logging.info('Removendo segmentos classificados através de REGEX...')
        qtd_seg = dados.limp['id_seg'].count()
        qtd_regex = dados.limp['tipo_seg'].isin(self.tipos_seg_padrao_regex).sum()
        dados.limp = dados.limp[~dados.limp['tipo_seg'].isin(self.tipos_seg_padrao_regex)]
        logging.info(f'Foram excluídos {qtd_regex} segmentos classificados por REGEX.')
        logging.info(f'Restaram {qtd_seg - qtd_regex} segmentos.')


    def remover_tags_html(self, dados):
        logging.info('Removendo tags HTML...')
        padrao_tag_html = re.compile('<.*?>')
        remover_tags = lambda txt : re.sub(padrao_tag_html, '', str(txt)) 
        dados.limp['txt_seg'] = dados.limp['txt_seg'].apply(remover_tags)
        
    
    def remover_escape_html(self, dados):
        logging.info('Removendo caracteres de escape HTML...')
        remover_escape_chars = lambda txt : html.unescape(txt)
        dados.limp['txt_seg'] = dados.limp['txt_seg'].apply(remover_escape_chars)
     

    def reclassificar_nao_identificados(self, dados, tipo_ato):
        logging.info('Reclassificando segmentos não identificados...')
        seg_ni = dados.limp[dados.limp['tipo_seg'] == 'Não Identificado']
        
        padrao_seg = dict()
        padrao_seg['Artigo'] = re.compile('^"{0,1}\s*(Art|ART)\.\s*')
        padrao_seg['Inciso'] = re.compile('^(\s*)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})(\s-|\s–)')
        padrao_seg['Alínea'] = re.compile('^(\s*)([a-z]\))')
        padrao_seg['Parágrafo'] = re.compile('^(\s*)(§|Parágrafo|Paragrafo)')
                
        for tipo_seg, padrao in padrao_seg.items():
            if tipo_seg in self.tipos_seg_por_tipo_ato[tipo_ato]:
                qtd_seg_reclassificaveis = seg_ni[seg_ni['txt_seg'].str.contains(padrao)].count()['id_seg']
                ids_reclassificaveis = seg_ni[seg_ni['txt_seg'].str.contains(padrao)]['id_seg']
                dados.limp.loc[dados.limp['id_seg'].isin(ids_reclassificaveis), 'tipo_seg'] = tipo_seg
                logging.info(f'{qtd_seg_reclassificaveis} segmentos reclassificados como {tipo_seg}.')
        

    def executar(self, dados, tipo_ato, reclassificar_nao_identificados):
        self.carregar_dados_originais(dados)
        self.remover_segmentos_nulos(dados)
        self.remover_segmentos_tipo_anexo(dados)
        self.determinar_tipos_segmento(dados, tipo_ato)
        self.remover_segmentos_filtro_tipo_ato(dados, tipo_ato)
        self.remover_segmentos_nao_representativos(dados, tipo_ato)
        self.remover_tags_html(dados)
        self.remover_escape_html(dados)
        
        if reclassificar_nao_identificados:
            self.reclassificar_nao_identificados(dados, tipo_ato)
        
        self.remover_segmentos_padrao_regex(dados)        
        logging.info('Limpeza de dados concluída.')
    

    def executar_seg(self, texto_seg):
        logging.info('Removendo tags HTML...')
        padrao_tag_html = re.compile('<.*?>')
        texto_seg = re.sub(padrao_tag_html, '', texto_seg)
        logging.info('Removendo caracteres de escape HTML...')
        texto_seg = html.unescape(texto_seg)
        return texto_seg