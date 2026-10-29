import random


def srtd(data, debug, sender):
    arguments = data.split("d")

    if len(arguments) < 2:
        return "Too small amount of arguments"

    if len(arguments) > 2:
        return "Too many arguments"

    arg1, arg2 = arguments

    if debug:
        print(sender + ":!rtd " + arg1 + "d" + arg2)

    arg1 = arg1.replace(" ", "")
    arg2 = arg2.replace(" ", "")

    try:
        i_arg1 = int(arg1)
        i_arg2 = int(arg2)
    except ValueError:
        return "You lied! That's not a number!"

    if i_arg1 == 0 or i_arg2 == 0:
        return "Too many zeroes!"

    if abs(i_arg1) > 500:
        return "Too many rolls, I can only do five hundred at max."

    die = []

    for _ in range(abs(i_arg1)):
        if i_arg2 < 0:
            dice = random.randint(i_arg2, 0)
        else:
            dice = random.randint(1, i_arg2)

        die.append(dice)

    return str(sum(die))