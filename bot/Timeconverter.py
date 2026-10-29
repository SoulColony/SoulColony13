import re
from decimal import Decimal, InvalidOperation


# Fixed offsets from the original file; not a date-aware timezone database.
times = {
    "ADT": -3, "HAA": -3, "AKDT": -8, "HAY": -8,
    "AKST": -9, "HNY": -9, "AST": -4, "HNA": -4,
    "CDT": -5, "HAC": -5, "CST": -6, "HNC": -6,
    "EDT": -4, "HAE": -4, "EGST": 0, "EGT": -1,
    "EST": -5, "HNE": -5, "ET": -5, "HADT": -9,
    "HAST": -10, "MDT": -6, "HAR": -6,
    "MST": -7, "HNR": -7, "NDT": -2.5, "HAT": -2.5,
    "NST": -3.5, "HNT": -3.5, "PDT": -7, "HAP": -7,
    "PMDT": -2, "PMST": -3, "PST": -8, "HNP": -8,
    "PT": -8, "WGST": -2, "WGT": -3, "GMT": 0, "UTC": 0,
}


def _zone_minutes(zone):
    match = re.fullmatch(r"([A-Z]+)(?:([+-])(.+))?", zone.strip().upper())
    if match is None:
        raise ValueError("Invalid zone syntax")

    base, sign, offset = match.groups()
    total = Decimal(str(times[base])) * 60
    if sign is None:
        return int(total)

    try:
        if ":" in offset:
            hours, minutes = offset.split(":")
            if not hours.isdigit() or not minutes.isdigit():
                raise ValueError("Invalid offset")
            minute_value = int(minutes)
            if not 0 <= minute_value < 60:
                raise ValueError("Invalid offset minutes")
            delta = Decimal(int(hours) * 60 + minute_value)
        else:
            if re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", offset) is None:
                raise ValueError("Invalid offset")
            delta = Decimal(offset) * 60
            if delta != delta.to_integral_value():
                raise ValueError("Offset requires fractional minutes")
    except InvalidOperation as exc:
        raise ValueError("Invalid offset") from exc

    return int(total + delta if sign == "+" else total - delta)


def converter(zones, time):
    try:
        from_z, to_z = zones
    except (TypeError, ValueError):
        return "Too many or too small amount of values"

    try:
        from_minutes = _zone_minutes(from_z)
    except KeyError:
        return "Incorrect From zone"
    except (ValueError, TypeError, AttributeError):
        return "Error, the 'From Zone' variable has an incorrect offset number"

    try:
        to_minutes = _zone_minutes(to_z)
    except KeyError:
        return "Incorrect To zone"
    except (ValueError, TypeError, AttributeError):
        return "Error, the 'To Zone' variable has an incorrect offset number"

    try:
        separator = ":" if ":" in time else "."
        hours, minutes = map(int, time.split(separator))
        if not 0 <= hours < 24 or not 0 <= minutes < 60:
            raise ValueError("Invalid clock time")
    except (TypeError, ValueError, AttributeError):
        return "The time was input in an odd way"

    total = hours * 60 + minutes + to_minutes - from_minutes
    hours, minutes = divmod(total, 60)
    return f"{hours}{separator}{minutes}"


def formatter(time):
    if "." in time:
        separator = "."
    elif ":" in time:
        separator = ":"
    else:
        return time

    try:
        hours, minutes = map(int, time.split(separator))
    except ValueError:
        return time

    days, remainder = divmod(hours * 60 + minutes, 24 * 60)
    hours, minutes = divmod(remainder, 60)
    result = f"{hours:02d}{separator}{minutes:02d}"

    if days == 1:
        return result + " (Tomorrow)"
    if days > 1:
        return result + f" (After {days} days)"
    if days == -1:
        return result + " (Yesterday)"
    if days < -1:
        return result + f" ({abs(days)} days ago)"
    return result
