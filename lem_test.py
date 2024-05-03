from textblob import Word
import nltk
import requests
from unidecode import unidecode

nltk.download("wordnet")

keyword = "trained"

req = requests.get(f"https://api.datamuse.com/words?rel_jja={keyword}&md=d&max=150")
resp = req.json()

words = [word["word"] for word in resp]

for index, word in enumerate(words[::-1]):
    w = Word(word)
    base = w.lemmatize()
    plural = Word(base).pluralize()
    print(index + 1, base, plural)
