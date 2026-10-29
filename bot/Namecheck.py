def Namecheck(name, against, sender):
    """Return True for a match, otherwise False."""
    lowered_name = name.lower()
    lowered_sender = sender.lower()

    for candidate in against:
        if candidate.lower() in lowered_name and lowered_sender not in lowered_name:
            return True

    return False


def Namecheck_dict(name, against):
    """Return (matched, key); an empty dictionary returns (False, None)."""
    lowered_name = name.lower()
    last_key = None

    for key, candidate in against.items():
        last_key = key
        if candidate.lower() in lowered_name:
            return True, key

    return False, last_key