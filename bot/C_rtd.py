import random


def rtd(data, debug, sender):
    try:
        arg1, arg2 = data.split("d")
    except ValueError:
        return "Too many or too small amount of arguments"

    if debug:
        print(sender + ":!rtd " + arg1 + "d" + arg2)

    die = []
    die2 = []
    current_mark = ""
    nicer_form = ""
    outcome = 0
    realnumberfound = False
    checks = []
    count = 0

    arg1 = arg1.replace(" ", "")
    arg2 = arg2.replace(" ", "")

    try:
        i_arg1 = int(arg1)
        a_arg1 = abs(i_arg1)

        if "+" in arg2 or "-" in arg2:
            plus_spot = arg2.find("+")
            minus_spot = arg2.find("-")

            if plus_spot == -1 and minus_spot == -1:
                nicer_form = ""
            elif plus_spot != -1 and minus_spot == -1:
                nicer_form = arg2[plus_spot:]
            elif plus_spot == -1 and minus_spot != -1:
                nicer_form = arg2[minus_spot:]
            elif plus_spot < minus_spot:
                nicer_form = arg2[plus_spot:]
            else:
                nicer_form = arg2[minus_spot:]

            for letter in arg2:
                if letter == "+" or letter == "-":
                    current_mark = letter
                    checks = []
                    count += 1
                    continue

                checks.append(letter)

                try:
                    next_up = arg2[count + 1]
                except IndexError:
                    if not realnumberfound:
                        i_arg2 = int("".join(checks))
                        checks = []
                        realnumberfound = True
                    elif current_mark == "+":
                        outcome += int("".join(checks))
                    else:
                        outcome -= int("".join(checks))
                else:
                    if next_up == "+" or next_up == "-":
                        if not realnumberfound:
                            i_arg2 = int("".join(checks))
                            checks = []
                            realnumberfound = True
                        else:
                            if current_mark == "+":
                                outcome += int("".join(checks))
                            else:
                                outcome -= int("".join(checks))
                            checks = []

                    count += 1

            if not realnumberfound:
                return "You lied! That's not a number!"
        else:
            i_arg2 = int(arg2)

        if a_arg1 == 0 or i_arg2 == 0:
            return "Too many zeroes!"

    except ValueError:
        return "You lied! That's not a number!"

    if a_arg1 > 100:
        return "Too many rolls, I can only do one hundred at max."

    for _ in range(a_arg1):
        if i_arg2 < 0:
            dice = random.randint(i_arg2, 0)
        else:
            dice = random.randint(1, i_arg2)

        die.append(dice)
        die2.append(str(dice))

    if i_arg2 < 0:
        flist = "".join(die2)
    else:
        flist = "+".join(die2)

    total = sum(die) + outcome

    if len(flist) > 350:
        return str(total)

    if current_mark == "":
        return flist + " = " + str(total)

    return flist + " (" + nicer_form + ") = " + str(total)