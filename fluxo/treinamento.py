import logging

class Treinamento:

    def __init__(self):
        self.classificadores = dict()
    
    def adicionar_modelo(self, classificador):
        self.classificadores[classificador.nome] = classificador

    def treinar_modelos(self, dados, cv=None):
        if not cv:
            logging.info('Treinando modelos...')
            for nome_classificador in self.classificadores:
                self.classificadores[nome_classificador].treinar(dados)
                self.classificadores[nome_classificador].calcular_metricas(dados)
        else:
            logging.info('Treinando modelos com cross-validation...')
            for nome_classificador in self.classificadores:
                self.classificadores[nome_classificador].executar_cross_validation(dados, cv)