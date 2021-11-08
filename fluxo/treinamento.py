import logging

class Treinamento:

    def __init__(self):
        self.classificadores = dict()
    
    def adicionar_modelo(self, classificador):
        self.classificadores[classificador.nome] = classificador

    def treinar_modelos(self, dados, cv=None):
        for nome_classificador in self.classificadores:
            if not cv:
                logging.info(f'Treinando modelo {nome_classificador}...')
                self.classificadores[nome_classificador].treinar_sem_cv(dados.Xtr, dados.Ytr, dados.Xte, dados.Yte, 
                                                                        dados.labels, dados.metricas)
                logging.info(f'Treinamento do modelo {nome_classificador} concluído.')
            else:
                logging.info(f'Treinando modelo {nome_classificador} com cross-validation...')
                self.classificadores[nome_classificador].treinar_com_cv(dados.X, dados.y, dados.labels, dados.metricas, cv)
                logging.info(f'Treinamento do modelo {nome_classificador} com cross-validation concluído.')