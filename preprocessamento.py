import logging
import spacy

class Preprocessamento:
    
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        logging.info("Carregando modelo de Português para preprocessamento...")
        self.nlp = spacy.load('pt_core_news_sm')
        
    def executarPipelinePreprocessamento(self, dados):
        logging.info("Executando pipeline de preprocessamento...")
        with self.nlp.select_pipes(enable=['tagger','lemmatizer']):
            dados.seg_prep = dados.seg_limp
            dados.seg_prep['docs'] = list(self.nlp.pipe(dados.seg_limp['txt_seg']))
            
    def executar(self, dados):
        self.executarPipelinePreprocessamento(dados)
        
