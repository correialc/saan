import logging
import nltk
from nltk.tokenize import WhitespaceTokenizer, RegexpTokenizer
from nltk.stem import SnowballStemmer
from string import punctuation

class Preprocessamento:
    
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        nltk.download('stopwords')
        self.stopwords = nltk.corpus.stopwords.words('portuguese')
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stemmer = SnowballStemmer('portuguese')
    
    def converter_para_minusculo(self, tokens):
        minusculo = map(str.lower, tokens)
        return list(minusculo)

    def remover_pontuacao(self, tokens):
        sem_pontuacao = filter(lambda token : token not in punctuation, tokens)
        return list(sem_pontuacao)

    def remover_stopwords(self, tokens):
        sem_stop_words = filter(lambda token : token not in self.stopwords, tokens)
        return list(sem_stop_words)

    def extrair_stems(self, tokens):
        tokens_stemmed = [self.stemmer.stem(token) for token in tokens]
        return tokens_stemmed

    def executar(self, dados):
        dados.prep = dados.limp.copy()
        logging.info('Realizando tokenização...')
        dados.prep['tokens'] = dados.prep['txt_seg'].apply(self.tokenizer.tokenize)
        logging.info('Convertendo caracteres para minúsculo...')
        dados.prep['tokens'] = dados.prep['tokens'].apply(self.converter_para_minusculo)
        logging.info('Removendo pontuação...')
        dados.prep['tokens'] = dados.prep['tokens'].apply(self.remover_pontuacao)
        logging.info('Removendo stopwords...')
        dados.prep['tokens'] = dados.prep['tokens'].apply(self.remover_stopwords)
        logging.info('Realizando stemming...')
        dados.prep['tokens'] = dados.prep['tokens'].apply(self.extrair_stems)
        logging.info('Preprocessamento concluído.')

        