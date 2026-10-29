parta = {
    "A": "N",
    "B": "O",
    "C": "P",
    "D": "Q",
    "E": "R",
    "F": "S",
    "G": "T",
    "H": "U",
    "I": "V",
    "J": "W",
    "K": "X",
    "L": "Y",
    "M": "Z",
}

partb = {
    "O": "B",
    "N": "A",
    "Q": "D",
    "P": "C",
    "S": "F",
    "R": "E",
    "U": "H",
    "T": "G",
    "W": "J",
    "V": "I",
    "Y": "L",
    "X": "K",
    "Z": "M",
}


def rot13(text):
    newtext = ""

    for letter in text:
        upper = letter.upper()
        replacement = parta.get(upper)

        if replacement is None:
            replacement = partb.get(upper)

        if replacement is None:
            newtext += letter
        elif letter.isupper():
            newtext += replacement
        else:
            newtext += replacement.lower()

    return newtext