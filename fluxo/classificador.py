from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

class Classificador:

    def __init__(self, nome, estimador):
        self.nome = nome
        self.estimador = estimador
    
    def treinar(self, dados):
        self.estimador.fit(dados.Xtr, dados.Ytr)

    def calcular_metricas(self, dados):
        y_predito = self.estimador.predict(dados.Xte)

        dados.metricas[self.nome] = {
            'acuracia': round(accuracy_score(dados.Yte, y_predito),4),
            'precisao': round(precision_score(dados.Yte, y_predito, pos_label=1, average='macro'),4),
            'revocacao': round(recall_score(dados.Yte, y_predito, pos_label=1, average='macro'), 4),
            'f1': round(f1_score(dados.Yte, y_predito, pos_label=1, average='macro'),4)
        }
