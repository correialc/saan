import logging
import joblib

class PersistenciaModelo:

    def __init__(self, tipo_ato):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt='%H:%M:%S')
        self.tipo_ato = tipo_ato
        self.caminho_modelos = './modelos/'

    def salvar_modelo(self, modelo):
        logging.info(f'Salvando modelo treinado para o tipo {self.tipo_ato}...')
        caminho_arquivo_modelo = (self.caminho_modelos+'classificador-segmentos-'+self.tipo_ato+'.mdl').lower()
        joblib.dump(modelo, caminho_arquivo_modelo)
        logging.info(f'Modelo salvo em {caminho_arquivo_modelo}.')