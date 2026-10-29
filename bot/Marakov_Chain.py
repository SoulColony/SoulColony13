import pickle
import random
from pathlib import Path

import CORE_DATA


DATA_DIR = Path("Marakov")
CACHE_PATH = DATA_DIR / "Marakov.Cache"
PUNCTUATION = "\",.?!'()[]{}"
STRIP_TABLE = str.maketrans("", "", ",.?!()[]\"'")
CONTINUATIONS = {
    "but", "who", "gets", "im", "most", "is", "it", "if", "then",
    "after", "over", "every", "of", "on", "or", "as", "the",
    "wheather", "whether", "a", "to", "and", "for",
}


def merge(d1, d2, merger=lambda x, y: x + y):
    result = dict(d1)

    for key, value in d2.items():
        if key in result:
            result[key] = merger(result[key], value)
        else:
            result[key] = value

    return result


def _load(path):
    with Path(path).open("rb") as source:
        data = pickle.load(source, encoding="latin1")

    if not isinstance(data, dict):
        raise ValueError("Expected a dictionary of word lists")

    if any(
        not isinstance(key, str)
        or not isinstance(values, list)
        or any(not isinstance(value, str) for value in values)
        for key, values in data.items()
    ):
        raise ValueError("Expected string keys and lists of strings")

    return data


def _save(path, data):
    with Path(path).open("wb") as destination:
        pickle.dump(data, destination)


def _is_url(word):
    word = word.lower()
    return word.startswith(
        ("http://", "https://", "www.", "http:" + "\\" * 2)
    )


full_data = {}
imported_data = {}
DATA_DIR.mkdir(parents=True, exist_ok=True)

for path in sorted(DATA_DIR.iterdir()):
    if not path.is_file() or "marakov." not in path.name.lower():
        continue

    loaded = _load(path)

    if path.name == "Marakov.Cache":
        old_size = len(full_data)
        full_data = merge(full_data, loaded)
        print("Added contents of " + path.name)
        print("Entries: " + str(len(full_data) - old_size))
    else:
        imported_data = merge(imported_data, loaded)
        print("Added contents of " + path.name + " (Import)")
        print("Entries: " + str(len(imported_data)))


def give_data(data):
    state = False
    words = data.split(" ")
    excluded = [CORE_DATA.prefix + "marakov"] + CORE_DATA.SName

    for a, b in zip(words, words[1:]):
        a = a.lower().translate(STRIP_TABLE)
        b = b.lower().translate(STRIP_TABLE)

        if a in excluded:
            continue

        state = True

        if _is_url(a):
            continue

        if a in full_data:
            if b not in full_data[a]:
                full_data[a].append(b)
        elif a not in imported_data:
            full_data[a] = [b]

    if state:
        _save(CACHE_PATH, full_data)


def form_sentence(argument=None):
    sentence = []

    for _ in range(20):
        if argument is not None:
            a = argument
        elif full_data:
            a = random.choice(list(full_data))
        elif imported_data:
            a = random.choice(list(imported_data))
        else:
            return "No sentences formable at all"

        sentence = [a]
        length = 0

        while length < 12 or (
            sentence[-1].lower() in CONTINUATIONS and length < 24
        ):
            options = full_data.get(a) or imported_data.get(a)
            if not options:
                break

            a = random.choice(options)
            sentence.append(a)
            length += 1

        if len(sentence) > 5:
            return sentence

    return sentence


def remdata(arg):
    if arg not in full_data:
        print("There is no such data")
        return

    del full_data[arg]
    _save(CACHE_PATH, full_data)


def remobject(arg1, arg2):
    try:
        full_data[arg1].remove(arg2)
    except ValueError:
        print("No such object")
    except KeyError:
        print("No such data")
    else:
        _save(CACHE_PATH, full_data)


def convert(filename_from, filename_to):
    try:
        data = _load(filename_from)
    except (OSError, EOFError, pickle.UnpicklingError, ValueError):
        print("Error!")
        return

    # Build a new dictionary instead of mutating keys during iteration.
    converted = {}

    for key, values in data.items():
        new_key = key

        if new_key and new_key[-1] in PUNCTUATION:
            new_key = new_key[:-1]

        new_key = new_key.lower()
        cleaned = []

        for value in values:
            if not value or _is_url(value):
                continue

            if value[-1] in PUNCTUATION:
                value = value[:-1]

            cleaned.append(value.lower())

        converted.setdefault(new_key, []).extend(cleaned)

    _save(filename_to, converted)