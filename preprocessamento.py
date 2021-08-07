import logging
import spacy

class Preprocessamento:
    
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        logging.info("Carregando modelo de Português para preprocessamento...")
        self.nlp = spacy.load('pt_core_news_sm')
        self.docs = []
        
    def executarPipelinePreprocessamento(self, dados):
        logging.info("Executando pipeline de preprocessanmento...")
        with self.nlp.select_pipes(enable=['tagger','lemmatizer']):
            self.docs = list(self.nlp.pipe(dados.seg_limp['txt_seg']))

    def executar(self, dados):
        self.executarPipelinePreprocessamento(dados)
        dados.seg_prep = dados.seg_limp
        dados.seg_prep['docs'] = self.docs
