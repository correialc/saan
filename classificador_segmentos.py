import sys
import logging
import pandas as pd
from string import punctuation
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from fluxo.dados import Dados
from fluxo.limpeza_dados import LimpezaDados
from fluxo.preprocessamento import Preprocessamento
from fluxo.extracao_caracteristicas import ExtracaoCaracteristicas
from fluxo.persistencia_modelo import PersistenciaModelo

class ClassificadorSegmentos:

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt='%H:%M:%S')
        
        persistencia = PersistenciaModelo()

        self.clf = dict()
        self.clf['ade'] = persistencia.carregar_modelo('ADE')
        self.clf['sc'] = persistencia.carregar_modelo('SC')
        self.clf['port'] = persistencia.carregar_modelo('Port.')

        self.vet = dict()
        self.vet['ade'] = persistencia.carregar_vetorizador('ADE')
        self.vet['sc'] = persistencia.carregar_vetorizador('SC')
        self.vet['port'] = persistencia.carregar_vetorizador('Port.')


    def classificar_segmentos(self, tipo_ato, dados):
        lp = LimpezaDados(dados)
        lp.executar(dados, tipo_ato, reclassificar_nao_identificados=True)
        pp = Preprocessamento()
        pp.executar(dados)
        
        tipo_ato = ''.join([caractere.lower() for caractere in tipo_ato if caractere not in punctuation])
        X = self.vet[tipo_ato].transform(dados.prep['texto'])

        logging.info('Classificando segmentos...')
        dados.pred = dados.prep
        dados.pred['tipo_seg_pred'] = self.clf[tipo_ato].predict(X)
        logging.info('Classificação concluída.')
        
        logging.info('Calculando métricas...')
        metricas = dict()
        metricas['acuracia'] = round(accuracy_score(dados.pred['tipo_seg'], dados.pred['tipo_seg_pred']),4)
        metricas['precisao'] = round(precision_score(dados.pred['tipo_seg'], dados.pred['tipo_seg_pred'], pos_label=1, average='macro'),4)
        metricas['revocacao'] = round(recall_score(dados.pred['tipo_seg'], dados.pred['tipo_seg_pred'], pos_label=1, average='macro'), 4)
        metricas['f1'] = round(f1_score(dados.pred['tipo_seg'], dados.pred['tipo_seg_pred'], pos_label=1, average='macro'),4)
        logging.info('Métricas calculadas')

        return dados.pred, metricas
        