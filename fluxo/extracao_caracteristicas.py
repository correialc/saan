import logging
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

class ExtracaoCaracteristicas:

    def __init__(self, dados):
        logging.basicConfig(level=logging.INFO)
        self.vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5, ngram_range=(1,2))
        dados.treino, dados.teste = train_test_split(dados.prep, test_size=0.20, stratify=dados.prep['tipo_seg'],
                                        shuffle=True)

    def vetorizar(self, dados):
        logging.info('Executando vetorização TF-IDF...')
        self.vectorizer.fit(dados.treino['texto'].to_list())

        dados.Xtr = self.vectorizer.transform(dados.treino['texto'].to_list())
        dados.Ytr = dados.treino['tipo_seg'].to_list()

        dados.Xte = self.vectorizer.transform(dados.teste['texto'].to_list())
        dados.Yte = dados.teste['tipo_seg'].to_list()
        
    def executar(self, dados):
        self.vetorizar(dados)
        tam_vocabulario = len(self.vectorizer.get_feature_names())
        logging.info(f'Tamanho do vocabulario: {tam_vocabulario} termos')
        logging.info('Extração de características concluída.')