from ._html_cleaner import clean_html
from ._spaces_cleaner import clean_spaces
from ._to_morpheme import text_to_morphems
from ._to_lower import to_lower_text
from ._emoji_cleaner import clean_emoji
from ._clean_stopwords import clean_stopwords
from ._punctuation_cleaner import clean_punctuation


class TextCleaner:
    def __init__(self, spaces=True, punctuation=True, html=True, emoji=True, lower=True,
                 stop_words=True, morpheme=True):

        """
        Метод __init__ инциализирует экземпляр класса TextCleaner

        self.spaces = spaces - Необходимо ли удалять пробелы
        self.punctuation = punctuation - Необходимо ли удалять пунктуацию
        self.html = html - Необходимо ли удалять теги HTML
        self.emoji = emoji - Необходимо ли удалять Emoji
        self.lower = lower - Необходимо ли переводить текст в нижний регистр
        self.stopwords = stop_words - Необходимо ли удалять стоп слова
        self.morpheme = morpheme - Необходимо ли заменять слова на морфемы

        """

        self.spaces = spaces
        self.punctuation = punctuation
        self.html = html
        self.emoji = emoji
        self.lower = lower
        self.stopwords = stop_words
        self.morpheme = morpheme

        self.to_lower = to_lower_text
        self.clean_emoji = clean_emoji
        self.clean_punctuation = clean_punctuation
        self.clean_html = clean_html
        self.clean_space = clean_spaces
        self.clean_stopwords = clean_stopwords
        self.to_morpheme = text_to_morphems

    def clean_text(self, text: str) -> str:

        """ Метод clean_text форматирует текст в зависимости от поставленных флагов"""

        if self.lower:
            text = self.to_lower(text)
        if self.emoji:
            text = self.clean_emoji(text)
        if self.html:
            text = self.clean_html(text)
        if self.punctuation:
            text = self.clean_punctuation(text)
        if self.stopwords:
            text = self.clean_stopwords(text)
        if self.morpheme:
            text = self.to_morpheme(text)
        if self.spaces:
            text = self.clean_space(text)

        return text

    def clean_texts(self, texts: []) -> []:

        clean_texts = []

        """ Метод clean_texts форматирует массив в зависимости от поставленных флагов"""

        for text in texts:
            if self.lower:
                text = self.to_lower(text)
            if self.emoji:
                text = self.clean_emoji(text)
            if self.html:
                text = self.clean_html(text)
            if self.punctuation:
                text = self.clean_punctuation(text)
            if self.stopwords:
                text = self.clean_stopwords(text)
            if self.morpheme:
                text = self.to_morpheme(text)
            if self.spaces:
                text = self.clean_space(text)
            clean_texts.append(text)

        return clean_texts

    def to_vector(self, text: str) -> []:
        return self.clean_text(text).split()

    def to_vectors(self, text: []) -> []:
        clean_texts = self.clean_texts(text)
        answer = []
        for t in clean_texts:
            answer.append(t.split())
        return answer