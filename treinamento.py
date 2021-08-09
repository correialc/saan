class Treinamento:

    def __init__(self):
        self.classificadores = dict()
    
    def adicionar_modelo(self, classificador):
        self.classificadores[classificador.nome] = classificador

    def treinar_modelos(self, dados):
        for nome_classificador in self.classificadores:
            self.classificadores[nome_classificador].treinar(dados)
            self.classificadores[nome_classificador].calcular_metricas(dados)