import requests
import time

attempt_index = 0


def find_word(ai):
    if ai == 3:
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
        req = requests.get(
            f"https://api.datamuse.com/words?rel_jja={keyword}&md=d&max=150"
        )
    except requests.exceptions.RequestException as e:
        return find_word(ai)

    resp = req.json()

    plurals = {}

    for word in resp:
        if word.get("defHeadword"):
            plurals.update(
                {
                    word["word"]: {
                        "score": word["score"],
                        "headword": word["defHeadword"],
                    }
                }
            )

    to_remove = []

    occurences_list = [metadata["headword"].lower() for metadata in plurals.values()]

    derivations = set()

    for item in occurences_list:
        if occurences_list.count(item) > 1:
            derivations.add(item)

    for rep_word in derivations:
        to_compare = []
        for plural, metadata in plurals.items():
            if metadata["headword"].lower() == rep_word:
                to_compare.append({plural: {"score": metadata["score"]}})
        score = 0
        for item in to_compare:
            for metadata in item.values():
                if metadata["score"] > score:
                    score = metadata["score"]
        for item in to_compare:
            for key, metadata in item.items():
                if metadata["score"] != score:
                    to_remove.append(key)
                    plurals.pop(key)

    for plural, metadata in plurals.items():
        for word in resp:
            if word["word"].lower() == metadata["headword"].lower():
                if word["score"] < metadata["score"]:
                    to_remove.append(word["word"])
                elif word["score"] > metadata["score"]:
                    to_remove.append(plural)

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

    if len(words) >= 50:
        words = words[:50]
        return {keyword: words}

    else:
        return find_word(ai)  # Need to get a new word


ret = find_word(attempt_index)

for key, value in ret.items():
    words = value
    keyword = key

with open("./src/words.txt", "w") as out:
    out.write(("\n").join(words))

with open("./src/keyword.txt", "w") as word:
    word.write(keyword)
