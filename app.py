import sys
import pandas as pd

from fluxo.dados import Dados
from fluxo.limpeza_dados import LimpezaDados
from fluxo.preprocessamento import Preprocessamento
from fluxo.extracao_caracteristicas import ExtracaoCaracteristicas

seg = sys.argv[1]
df = pd.DataFrame(data={'txt_seg':[seg]})
print(df)

