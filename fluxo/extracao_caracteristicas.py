import logging
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE

class ExtracaoCaracteristicas:

    def __init__(self, dados):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt='%H:%M:%S')
        self.vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5, ngram_range=(1,2))
        

    def vetorizar(self, dados):
        logging.info('Executando vetorização TF-IDF...')
        self.vectorizer.fit(dados.prep['texto'].to_list())

        dados.treino, dados.teste = train_test_split(
                                        dados.prep, test_size=0.20, 
                                        stratify=dados.prep['tipo_seg'],
                                        shuffle=True, random_state=dados.random_state)

        dados.Xtr = self.vectorizer.transform(dados.treino['texto'].to_list())
        dados.Ytr = dados.treino['tipo_seg'].to_list()

        dados.Xte = self.vectorizer.transform(dados.teste['texto'].to_list())
        dados.Yte = dados.teste['tipo_seg'].to_list()


    def vetorizar_cv(self, dados, oversampling):
        logging.info('Executando vetorização TF-IDF para Cross-Validation...')
        self.vectorizer.fit(dados.prep['texto'])
        dados.X = self.vectorizer.transform(dados.prep['texto'])
        dados.y = dados.prep['tipo_seg']

        if oversampling:
            smote = SMOTE(random_state=dados.random_state)
            dados.X, dados.y = smote.fit_resample(dados.X,dados.y)


    def executar(self, dados, oversampling):
        self.vetorizar(dados)
        self.vetorizar_cv(dados, oversampling)
        logging.info('Extração de características concluída.')