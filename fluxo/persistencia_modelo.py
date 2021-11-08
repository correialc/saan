import logging
import joblib
from string import punctuation

class PersistenciaModelo:

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt='%H:%M:%S')
        self.caminho_modelos = './modelos/'


    def salvar_modelo(self, modelo, tipo_ato):
        logging.info(f'Salvando modelo treinado para o tipo {tipo_ato}...')
        tipo_ato = ''.join([caractere.lower() for caractere in tipo_ato if caractere not in punctuation])
        caminho_arquivo_modelo = (self.caminho_modelos+'classificador-segmentos-'+tipo_ato+'.mdl')
        joblib.dump(modelo, caminho_arquivo_modelo)
        logging.info(f'Modelo salvo em {caminho_arquivo_modelo}.')


    def carregar_modelo(self, tipo_ato):
        logging.info(f'Carregando modelo treinado para o tipo {tipo_ato}...')
        tipo_ato = ''.join([caractere.lower() for caractere in tipo_ato if caractere not in punctuation])
        caminho_arquivo_modelo = (self.caminho_modelos+'classificador-segmentos-'+tipo_ato+'.mdl')
        return joblib.load(caminho_arquivo_modelo)


    def salvar_vetorizador(self, vetorizador, tipo_ato):
        logging.info(f'Salvando vetorizador para o tipo {tipo_ato}...')
        tipo_ato = ''.join([caractere.lower() for caractere in tipo_ato if caractere not in punctuation])
        caminho_arquivo_modelo = (self.caminho_modelos+'vetorizador-'+tipo_ato+'.mdl')
        joblib.dump(vetorizador, caminho_arquivo_modelo)
        logging.info(f'Vetorizador salvo em {caminho_arquivo_modelo}.')

    
    def carregar_vetorizador(self, tipo_ato):
        logging.info(f'Carregando vetorizador treinado para o tipo {tipo_ato}...')
        tipo_ato = ''.join([caractere.lower() for caractere in tipo_ato if caractere not in punctuation])
        caminho_arquivo_modelo = (self.caminho_modelos+'vetorizador-'+tipo_ato+'.mdl')
        return joblib.load(caminho_arquivo_modelo)