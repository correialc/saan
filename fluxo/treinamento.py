import logging

class Treinamento:

    def __init__(self):
        self.classificadores = dict()
    
    def adicionar_modelo(self, classificador):
        self.classificadores[classificador.nome] = classificador

    def treinar_modelos(self, dados, cv=None):
        if not cv:
            for nome_classificador in self.classificadores:
                logging.info(f'Treinando modelo {nome_classificador}...')
                self.classificadores[nome_classificador].treinar(dados)
                self.classificadores[nome_classificador].calcular_metricas(dados)
                logging.info(f'Treinamento do modelo {nome_classificador} concluído.')
        else:
            for nome_classificador in self.classificadores:
                logging.info(f'Treinando modelo {nome_classificador} com cross-validation...')
                self.classificadores[nome_classificador].executar_cross_validation(dados, cv)
                logging.info(f'Treinamento do modelo {nome_classificador} com cross-validation concluído.')