from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import cross_validate, cross_val_predict
from matplotlib import pyplot as plt

class Classificador:

    def __init__(self, nome, estimador):
        self.nome = nome
        self.estimador = estimador
        self.matriz_confusao = None
    

    def treinar_sem_cv(self, dados):
        self.estimador.fit(dados.Xtr, dados.Ytr)
        y_predito = self.estimador.predict(dados.Xte)

        dados.metricas[self.nome] = {
            'acuracia': round(accuracy_score(dados.Yte, y_predito),4),
            'precisao': round(precision_score(dados.Yte, y_predito, pos_label=1, average='macro'),4),
            'revocacao': round(recall_score(dados.Yte, y_predito, pos_label=1, average='macro'), 4),
            'f1': round(f1_score(dados.Yte, y_predito, pos_label=1, average='macro'),4)
            }

        y_predito = self.estimador.predict(dados.Xte)
        self.matriz_confusao = confusion_matrix(dados.Yte, y_predito, labels=dados.labels)


    def treinar_com_cv(self, dados, cv):
        resultado_cv = cross_validate(self.estimador, dados.X, dados.y, cv=cv, 
                        scoring=('accuracy', 'precision_macro', 'recall_macro', 'f1_macro'))
                
        dados.metricas[self.nome] = {
            'acuracia': round(resultado_cv['test_accuracy'].mean(), 4),
            'precisao': round(resultado_cv['test_precision_macro'].mean(), 4),
            'revocacao': round(resultado_cv['test_recall_macro'].mean(), 4),
            'f1': round(resultado_cv['test_f1_macro'].mean(), 4)
        }

        y_predito = cross_val_predict(self.estimador, dados.X, dados.y, cv=cv)
        self.matriz_confusao = confusion_matrix(dados.y, y_predito, labels=dados.labels)


    def plotar_matriz_confusao(self, dados):
        plt.rcParams.update({'font.size': 14})
        fig, ax = plt.subplots(figsize=(20,12))
        
        disp = ConfusionMatrixDisplay(confusion_matrix=self.matriz_confusao,
                                display_labels=dados.labels)
        disp.plot(cmap='Blues', ax=ax)
