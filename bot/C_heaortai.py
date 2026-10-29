# Throws a coin, simple.
from random import random


def heaortai(debug, sender):
    return "Heads" if random() > 0.5 else "Tails"


# This file used to be a lot bigger, now it's kind of useless.