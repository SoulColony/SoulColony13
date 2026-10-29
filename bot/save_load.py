import pickle


def save(filename, data, dnrw=0):
    mode = "xb" if dnrw == 1 else "wb"

    if isinstance(data, str):
        data = data.replace("http//", "http://")

    try:
        with open(filename, mode) as destination:
            pickle.dump(data, destination)
    except FileExistsError:
        if dnrw == 1:
            return False
        raise


def load(filename):
    try:
        source = open(filename, "rb")
    except OSError:
        return "ERROR ERROR ERROR ERR"

    with source:
        return pickle.load(source, encoding="latin1")