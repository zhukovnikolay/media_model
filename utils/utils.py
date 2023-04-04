from pymorphy3 import MorphAnalyzer
import re
from string import punctuation
from nltk.corpus import stopwords

STOPWORDS = stopwords.words('russian')
STOPWORDS.extend(['это', 'такой', 'который', 'свой', 'всё', 'ещё'])
NOISE = STOPWORDS + list(punctuation)


class CustomTokenizer:
    """
    Обрабатывает передаваемый документ.
    1. Приводит все слова к нижнему регистру
    2. Удаляет @ и # теги
    3. Удаляет пунктуацию и стоп-слова
    4. Лемматизирует
    5. Токенизирует
    """

    def __init__(self):
        self.lemmatizer = MorphAnalyzer(lang='ru')
        #        self.regexp = re.compile(r'\\.?|#.*? |[^а-яa-zёé’* ]|[a-z]*?\.[a-z].*? ')
        self.regexp = re.compile(r'\\.?|#.*? |[^а-яё* ]')

    def __call__(self, doc):
        # приводим текст к нижнему регистру и обрабатываем сокращенные слова

        doc_tokens = re.sub(self.regexp, ' ', doc.lower()).split()

        doc_tokens = [self.lemmatizer.normal_forms(word)[0]
                      for word in doc_tokens]

        doc_tokens = [token for token in doc_tokens
                      if token not in NOISE and len(token) > 2]

        return doc_tokens


def check_obscene(message: str, vocab: list = []) -> bool:
    """
    Проверяет наличие мата в посте
    """
    for token in message.split():
        if token in vocab:
            return True
    return False
