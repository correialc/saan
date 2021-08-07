import logging
import spacy
import nltk
from string import punctuation

class Preprocessamento:
    
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        logging.info("Carregando modelo de Português para preprocessamento...")
        self.nlp = spacy.load('pt_core_news_sm')
        nltk.download('stopwords')
        self.stopwords = nltk.corpus.stopwords.words('portuguese')
                
    def executar_pipeline_preprocessamento(self, dados):
        logging.info("Executando pipeline de preprocessamento...")
        with self.nlp.select_pipes(enable=['tagger','lemmatizer']):
            dados.prep = dados.limp
            dados.prep['docs'] = list(self.nlp.pipe(dados.limp['txt_seg']))
            logging.info("Salvando resultado da tokenização...")
            dados.prep['tokens'] = dados.prep['docs'].apply(self.salvar_tokens)

    def salvar_tokens(self, doc):
        termos = []
        for token in doc:
            termos.append(token.text)
        return termos
    
    def converter_para_minusculo(self, tokens):
        minusculo = map(str.lower, tokens)
        return list(minusculo)

    def remover_pontuacao(self, tokens):
        sem_pontuacao = filter(lambda token : token not in punctuation, tokens)
        return list(sem_pontuacao)

    def remover_stopwords(self, tokens):
        sem_stop_words = filter(lambda token : token not in self.stopwords, tokens)
        return list(sem_stop_words)

    def executar(self, dados):
        self.executar_pipeline_preprocessamento(dados)
        logging.info('Convertendo caracteres para minúsculo...')
        dados.prep['tokens'] = dados.prep['tokens'].apply(self.converter_para_minusculo)
        logging.info('Removendo pontuação...')
        dados.prep['tokens'] = dados.prep['tokens'].apply(self.remover_pontuacao)
        logging.info('Removendo stopwords...')
        dados.prep['tokens'] = dados.prep['tokens'].apply(self.remover_stopwords)

        