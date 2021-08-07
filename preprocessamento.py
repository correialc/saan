import logging
import spacy
from string import punctuation

class Preprocessamento:
    
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        logging.info("Carregando modelo de Português para preprocessamento...")
        self.nlp = spacy.load('pt_core_news_sm')
                
    def executar_pipeline_preprocessamento(self, dados):
        logging.info("Executando pipeline de preprocessamento...")
        with self.nlp.select_pipes(enable=['tagger','lemmatizer']):
            dados.seg_prep = dados.seg_limp
            dados.seg_prep['docs'] = list(self.nlp.pipe(dados.seg_limp['txt_seg']))
            logging.info("Salvando resultado da tokenização...")
            dados.seg_prep['tokens'] = dados.seg_prep['docs'].apply(self.salvar_tokens)

    def salvar_tokens(self, doc):
        termos = []
        for token in doc:
            termos.append(token.text)
        return termos
    
    def converter_para_minusculo(self, tokens):
        minusculo = map(str.lower, tokens)
        return list(minusculo)

    def executar(self, dados):
        self.executar_pipeline_preprocessamento(dados)
        logging.info('Convertendo caracteres para minúsculo...')
        dados.seg_prep['tokens'] = dados.seg_prep['tokens'].apply(self.converter_para_minusculo)
        