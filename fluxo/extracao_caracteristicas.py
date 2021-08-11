import logging
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

class ExtracaoCaracteristicas:

    def __init__(self, dados):
        logging.basicConfig(level=logging.INFO)
        self.vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5, ngram_range=(1,2))
        

    def vetorizar(self, dados):
        logging.info('Executando vetorização TF-IDF...')
        self.vectorizer.fit(dados.prep['texto'].to_list())

        dados.treino, dados.teste = train_test_split(dados.prep, test_size=0.20, stratify=dados.prep['tipo_seg'],
                                        shuffle=True, random_state=dados.random)

        dados.Xtr = self.vectorizer.transform(dados.treino['texto'].to_list())
        dados.Ytr = dados.treino['tipo_seg'].to_list()

        dados.Xte = self.vectorizer.transform(dados.teste['texto'].to_list())
        dados.Yte = dados.teste['tipo_seg'].to_list()

    def vetorizar_cv(self, dados):
        logging.info('Executando vetorização TF-IDF para Cross-Validation...')
        self.vectorizer.fit(dados.prep['texto'].to_list())
        dados.X = self.vectorizer.transform(dados.prep['texto'].to_list())
        dados.y = dados.prep['tipo_seg']

    def executar(self, dados):
        self.vetorizar(dados)
        self.vetorizar_cv(dados)
        logging.info('Extração de características concluída.')