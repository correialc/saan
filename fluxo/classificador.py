from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import cross_validate
from matplotlib import pyplot as plt

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

    def executar_cross_validation(self, dados, cv):
        resultado_cv = cross_validate(self.estimador, dados.X, dados.y, cv=cv, 
                        scoring=('accuracy', 'precision_macro', 'recall_macro', 'f1_macro'))
                
        dados.metricas[self.nome] = {
            'acuracia': round(resultado_cv['test_accuracy'].mean(), 4),
            'precisao': round(resultado_cv['test_precision_macro'].mean(), 4),
            'revocacao': round(resultado_cv['test_recall_macro'].mean(), 4),
            'f1': round(resultado_cv['test_f1_macro'].mean(), 4)
        }

    def plotar_matriz_confusao(self, dados):
        plt.rcParams.update({'font.size': 14})
        fig, ax = plt.subplots(figsize=(20,12))

        y_predito = self.estimador.predict(dados.Xte)
        cm = confusion_matrix(dados.Yte, y_predito, labels=self.estimador.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                display_labels=self.estimador.classes_)
        disp.plot(cmap='Blues', ax=ax)
