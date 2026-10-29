# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from urllib.request import urlopen


# S10 COMPATIBLE
def message(data):
    if data["type"] != "PRIVMSG":
        return -1

    try:
        splitdata = data["content"].lower().split(" ")
        if splitdata[0] == ":weather" and len(splitdata) > 1:
            weather_result = Weather(" ".join(splitdata[1:]))

            data["conn"].privmsg(
                data["target"],
                "Weather for " + weather_result[1] + ": " + weather_result[0],
            )
            return True
    except KeyError:
        print("WUT")


def Weather(question):
    question = question.replace("\u00e4", "a")
    query = urlencode({"query": question})
    url = (
        "http://api.wunderground.com/auto/wui/geo/"
        "WXCurrentObXML/index.xml?" + query
    )

    with urlopen(url, timeout=15) as response:
        encoding = response.headers.get_content_charset() or "utf-8"
        weather_data = response.read().decode(encoding, errors="replace")

    bufferi = []
    seen = False
    where = "Unknown location"

    for line in weather_data.splitlines():
        if "<temperature_string>" in line:
            stuff = cutter(line, "<temperature_string>")
            if len(stuff) > 7:
                bufferi.append("Temperature: " + stuff)
        elif "<observation_time>" in line:
            stuff = cutter(line, "<observation_time>")
            if len(stuff) > 19:
                bufferi.append(stuff)
        elif "<weather>" in line:
            stuff = cutter(line, "<weather>")
            if len(stuff) > 0:
                bufferi.append("Weather: " + stuff)
        elif "<relative_humidity>" in line:
            stuff = cutter(line, "<relative_humidity>")
            if len(stuff) > 0:
                bufferi.append("Humidity: " + stuff)
        elif "<wind_string>" in line:
            stuff = cutter(line, "<wind_string>")
            if len(stuff) > 0:
                bufferi.append("Wind blows " + stuff)
        elif "<pressure_string>" in line:
            stuff = cutter(line, "<pressure_string>")
            if len(stuff) > 9:
                bufferi.append("Air pressure is " + stuff)
        elif "<full>" in line and not seen:
            seen = True
            where = cutter(line, "<full>")
            if len(where) == 4:
                where = "Location doesn't exist"

    return [", ".join(bufferi), where]


def cutter(fullstring, cut):
    fullstring = fullstring.replace(cut, "")
    fullstring = fullstring.replace("</" + cut[1:], "")
    fullstring = fullstring.replace("\t", "")
    return fullstring