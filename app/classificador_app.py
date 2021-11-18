import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd

from fluxo.dados import Dados
from fluxo.limpeza_dados import LimpezaDados
from fluxo.preprocessamento import Preprocessamento
from fluxo.extracao_caracteristicas import ExtracaoCaracteristicas
from fluxo.persistencia_modelo import PersistenciaModelo

# Carrengando em mémória os modelos previamente treinados e persistidos
persistencia = PersistenciaModelo('../modelos/')

clf = dict()
clf['ade'] = persistencia.carregar_modelo('ADE')
clf['sc'] = persistencia.carregar_modelo('SC')
clf['port'] = persistencia.carregar_modelo('Port.')

vet = dict()
vet['ade'] = persistencia.carregar_vetorizador('ADE')
vet['sc'] = persistencia.carregar_vetorizador('SC')
vet['port'] = persistencia.carregar_vetorizador('Port.')

tipo_ato = sys.argv[1]
texto_seg = sys.argv[2]

lp = LimpezaDados()
texto_seg = lp.executar_seg(texto_seg)
