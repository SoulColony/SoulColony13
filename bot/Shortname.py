def shortname(name):
    lowname = name.lower()
    count = 0
    spot = 0

    for index, letter in enumerate(name):
        if letter.isupper():
            spot = index
            count += 1

    if "_" in name:
        if name.count("_") > 1:
            name = " ".join(name.split("_")[:name.count("_")])
            if name.lower()[-3:] == "the":
                return name[:-4]
            return name

        return name.split("_")[0]

    if count > 1 and len(name[:spot]) > 2:
        return name[:spot]

    if len(name) < 5:
        return name

    if any(fragment in lowname for fragment in ("ca", "ct", "tp", "lp")):
        end = max(
            lowname.find(fragment)
            for fragment in ("ca", "ct", "tp", "lp")
        )
        return name[:end + 1]

    return name[:len(name) // 2 + len(name) % 2]