import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd

from fluxo.dados import Dados
from fluxo.limpeza_dados import LimpezaDados
from fluxo.preprocessamento import Preprocessamento
from fluxo.persistencia_modelo import PersistenciaModelo

class ClassificadorBackend:

    def __init__(self, caminho_modelos):
        self.clf, self.vet = self.carregar_modelos_treinados(caminho_modelos)

    
    def carregar_modelos_treinados(self, caminho_modelos):
        persistencia = PersistenciaModelo(caminho_modelos)

        clf = dict()
        clf['ade'] = persistencia.carregar_modelo('ADE')
        clf['sc'] = persistencia.carregar_modelo('SC')
        clf['port'] = persistencia.carregar_modelo('Port.')

        vet = dict()
        vet['ade'] = persistencia.carregar_vetorizador('ADE')
        vet['sc'] = persistencia.carregar_vetorizador('SC')
        vet['port'] = persistencia.carregar_vetorizador('Port.')

        return clf, vet
    

    def classificar_segmento(self, tipo_ato, texto_seg):
        texto_seg = LimpezaDados().executar_seg(texto_seg)
        texto_seg = Preprocessamento().executar_seg(texto_seg)
        vetor_seg = self.vet[tipo_ato].transform([texto_seg])
        return self.clf[tipo_ato].predict(vetor_seg)