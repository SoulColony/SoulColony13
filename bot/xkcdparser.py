import json
import pickle
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import urlopen

from CORE_DATA import directory, no_absolute_paths


def xkcd(link):
    try:
        normalized = link.strip().replace("\\", "/")
        if "://" not in normalized:
            normalized = "https://" + normalized

        parsed = urlsplit(normalized)

        if parsed.scheme.lower() not in ("http", "https"):
            return "NOTHING"

        if (parsed.hostname or "").lower() not in (
            "xkcd.com",
            "www.xkcd.com",
        ):
            return "NOTHING"

        comic = parsed.path.strip("/")

        if comic and (not comic.isascii() or not comic.isdigit()):
            return "NOTHING"

        if comic:
            comic = str(int(comic))
            if comic == "0":
                return "NOTHING"

    except (AttributeError, TypeError, ValueError):
        return "NOTHING"

    cache_dir = (
        Path("xkcdcache")
        if no_absolute_paths
        else Path(directory) / "xkcdcache"
    )
    cache_path = cache_dir / comic if comic else None

    if cache_path is not None:
        try:
            with cache_path.open("rb") as cache_file:
                cached = pickle.load(cache_file, encoding="latin1")

            if isinstance(cached, str):
                return cached

        except (
            OSError,
            EOFError,
            pickle.UnpicklingError,
            ValueError,
            TypeError,
            ImportError,
            AttributeError,
        ):
            pass

    url = "https://xkcd.com/"
    if comic:
        url += comic + "/"
    url += "info.0.json"

    try:
        with urlopen(url, timeout=15) as response:
            title = json.loads(response.read())["title"]

        if not isinstance(title, str):
            return "NOTHING"

    except (URLError, OSError, ValueError, KeyError, TypeError):
        return "NOTHING"

    if cache_path is not None:
        try:
            cache_dir.mkdir(parents=True, exist_ok=True)

            with cache_path.open("wb") as cache_file:
                pickle.dump(title, cache_file)

        except (OSError, pickle.PicklingError):
            pass

    return title