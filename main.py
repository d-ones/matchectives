import requests
from textblob import Word
import nltk
import json
from unidecode import unidecode

attempt_index = 0
nltk.download("wordnet")


def find_word(ai):
    if ai == 5:
        raise Exception
    else:
        ai += 1

    with open("index.txt", "r") as i:
        index = int(i.read())

    index += 1

    with open("index.txt", "w") as i2:
        i2.write(str(index))

    with open("./res.txt") as adj:
        keywords = adj.readlines()

    keyword = keywords[index]
    keyword = keyword.strip("\n")

    try:
        req = requests.get(f"https://api.datamuse.com/words?rel_jja={keyword}&max=150")
    except requests.exceptions.RequestException as e:
        return find_word(ai)

    resp = req.json()

    to_remove = []

    words = [word["word"] for word in resp]

    for word in words:
        if " " in word:
            to_remove.append(word)
        if "-" in word:
            to_remove.append(word)

    for entry in to_remove:
        try:
            words.remove(entry)
        except ValueError:
            pass

    words_flattened = []

    for word in words:
        w = Word(word)
        base = w.lemmatize()
        if base not in words_flattened:
            words_flattened.append(base)

    if len(words_flattened) >= 50:
        score_dict = {}
        words_flattened = words_flattened[:50]
        for index, word in enumerate(words_flattened[::-1]):
            plural = Word(word).pluralize()
            score_dict.update({index + 1: [word, plural]})
        return {keyword: score_dict}

    else:
        return find_word(ai)  # Need to get a new word


ret = find_word(attempt_index)

for key, value in ret.items():
    words = value
    keyword = key

with open("./src/words.json", "w") as out:
    json.dump(words, out)

with open("./src/keyword.txt", "w") as word:
    word.write(keyword)
