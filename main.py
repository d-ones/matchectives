import requests

keyword = "purple"

req = requests.get(f"https://api.datamuse.com/words?rel_jja={keyword}&md=d&max=150")

resp = req.json()

plurals = {}

for word in resp:
    if word.get("defHeadword"):
        plurals.update(
            {word["word"]: {"score": word["score"], "headword": word["defHeadword"]}}
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
        print(item)
        for key, metadata in item.items():
            if metadata["score"] != score:
                to_remove.append(key)
                plurals.pop(key)
                print(key)


for plural, metadata in plurals.items():
    for word in resp:
        if word["word"].lower() == metadata["headword"].lower():
            if word["score"] < metadata["score"]:
                to_remove.append(word["word"])
            elif word["score"] > metadata["score"]:
                to_remove.append(plural)


words = [word["word"] for word in resp]

for entry in to_remove:
    try:
        words.remove(entry)
    except ValueError:
        pass

if len(words) >= 50:
    words = words[:50]

else:
    raise Exception("Not enough words")  # Need to get a new word

with open("./src/words.txt", "w") as out:
    out.write(("\n").join(words))

with open("./src/keyword.txt", "w") as word:
    word.write(keyword)
