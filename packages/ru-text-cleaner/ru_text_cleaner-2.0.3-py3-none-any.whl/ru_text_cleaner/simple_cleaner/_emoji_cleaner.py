import emoji

def clean_emoji(text: str) -> str:
    """
        Функция clean_emoji удаляет все emoji из текста
    """

    return ''.join(t for t in text if not emoji.is_emoji(t))
