from os import listdir

import CORE_DATA
from save_load import save


directory = CORE_DATA.directory


def mkquote(prefix, influx, sender, debug):
    arg = influx[10 + len(prefix):]

    if debug:
        print(
            sender + ":" + prefix + "makequote "
            + str(len(arg)) + " Characters"
        )

    if len(arg) == 0:
        return "Type something to a quote"

    files = listdir(directory + "userquotes")
    numb = 0

    while True:
        numb += 1
        filename = sender.lower() + str(numb)

        if filename not in files:
            save(
                directory + "userquotes/" + filename,
                [arg, sender.lower()],
            )
            return "Saved as:" + filename