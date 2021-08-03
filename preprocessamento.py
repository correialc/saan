import logging
import spacy
import pt_core_news_sm  

class Preprocessamento:

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.nlp = pt_core_news_sm.load()
        