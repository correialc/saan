import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classificador_backend import ClassificadorBackend

backend = ClassificadorBackend('../modelos/')

tipo_ato = sys.argv[1].lower()
texto_seg = sys.argv[2]

predito = backend.classificar_segmento(tipo_ato, texto_seg)
print(predito)