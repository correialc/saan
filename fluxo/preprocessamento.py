import logging
import nltk
from nltk.tokenize import WhitespaceTokenizer, RegexpTokenizer
from nltk.stem import SnowballStemmer
from string import punctuation

class Preprocessamento:
    
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt='%H:%M:%S')
        nltk.download('stopwords')
        self.stopwords = nltk.corpus.stopwords.words('portuguese')
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stemmer = SnowballStemmer('portuguese')
        self.tam_min_token = 2
    
    def remover_pontuacao(self, texto):
        return ''.join([caractere for caractere in texto if caractere not in punctuation])

    def remover_stopwords(self, tokens):
        return [token for token in tokens if token not in self.stopwords]

    def remover_tokens_pequenos(self, tokens):
        return [token for token in tokens if len(token) >= self.tam_min_token]

    def extrair_stems(self, tokens):
        tokens_stemmed = [self.stemmer.stem(token) for token in tokens]
        return tokens_stemmed

    def reconstruir_texto(self, tokens):
        return ' '.join(tokens)

    def executar(self, dados):
        dados.prep = dados.limp.copy()
        dados.prep['texto'] = dados.prep['txt_seg']
        logging.info('Convertendo caracteres para minúsculo...')
        dados.prep['texto'] = dados.prep['texto'].apply(str.lower)
        logging.info('Removendo pontuação...')
        dados.prep['texto'] = dados.prep['texto'].apply(self.remover_pontuacao)
        logging.info('Realizando tokenização...')
        dados.prep['tokens'] = dados.prep['texto'].apply(self.tokenizer.tokenize)
        logging.info('Removendo stopwords...')
        dados.prep['tokens'] = dados.prep['tokens'].apply(self.remover_stopwords)
        #logging.info('Realizando stemming...')
        #dados.prep['tokens'] = dados.prep['tokens'].apply(self.extrair_stems)
        logging.info(f'Removendo tokens menores que {self.tam_min_token} caracteres...')
        dados.prep['tokens'] = dados.prep['tokens'].apply(self.remover_tokens_pequenos)
        logging.info('Reconstruindo texto a partir dos tokens...')
        dados.prep['texto'] = dados.prep['tokens'].apply(self.reconstruir_texto)
        logging.info('Preprocessamento concluído.')


    def executar_seg(self, texto_seg):
        logging.info('Convertendo caracteres para minúsculo...')
        texto_seg = texto_seg.lower()
        logging.info('Removendo pontuação...')
        texto_seg = self.remover_pontuacao(texto_seg)
        logging.info('Realizando tokenização...')
        tokens = self.tokenizer.tokenize(texto_seg)
        logging.info('Removendo stopwords...')
        tokens = self.remover_stopwords(tokens)
        logging.info(f'Removendo tokens menores que {self.tam_min_token} caracteres...')
        tokens = self.remover_tokens_pequenos(tokens)
        logging.info('Reconstruindo texto a partir dos tokens...')
        texto_seg_processado = self.reconstruir_texto(tokens)
        logging.info('Preprocessamento concluído.')

        return texto_seg_processado
