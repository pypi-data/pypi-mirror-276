from src.ru_text_cleaner import TensorCleaner
from src.ru_text_cleaner import SimpleCleaner
import tensorflow

simple = SimpleCleaner()
tensor = TensorCleaner()

print(SimpleCleaner().clean_text('Как дела мудак ебаный? «Хуй»'))




