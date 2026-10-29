import hashlib
import pickle
import time
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from CORE_DATA import directory, no_absolute_paths


class _VideoTitleParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "meta":
            return

        attributes = dict(attrs)
        name = attributes.get("name", "").lower()
        property_name = attributes.get("property", "").lower()
        content = attributes.get("content")

        if content is None:
            return

        if name == "title":
            self.title = content
        elif property_name == "og:title" and self.title is None:
            self.title = content


def YTCV2(youtube_url, cache=1, debug=0):
    """Cache 0 disables caching; cache 1 enables caching."""
    cache_path = None

    if cache == 1:
        cache_key = hashlib.md5(
            youtube_url.encode("utf-8"),
            usedforsecurity=False,
        ).hexdigest()

        if no_absolute_paths:
            cache_dir = Path("YTCache")
        else:
            cache_dir = Path(directory) / "NanoTrasen" / "YTCache"

        cache_path = cache_dir / cache_key

        try:
            with cache_path.open("rb") as cache_file:
                cached = pickle.load(cache_file, encoding="latin1")

            if (
                isinstance(cached, (list, tuple))
                and len(cached) >= 1
                and isinstance(cached[0], str)
            ):
                return cached[0]
        except (
            OSError,
            EOFError,
            pickle.UnpicklingError,
            ValueError,
            TypeError,
            ImportError,
            AttributeError,
        ) as exc:
            if debug:
                print("YouTube cache read failed:", exc)

    youtube_url = youtube_url.replace("http//", "http://", 1).strip()

    if youtube_url.lower().startswith("www."):
        youtube_url = "https://" + youtube_url

    if youtube_url.count("/") + youtube_url.count("\\") < 3:
        return "Reflex: Video cannot exist"

    if not youtube_url.lower().startswith(("http://", "https://")):
        return "Reflex: Incorrect link start"

    try:
        with urlopen(youtube_url, timeout=15) as website:
            encoding = website.headers.get_content_charset() or "utf-8"
            page = website.read().decode(encoding, errors="replace")
    except (URLError, OSError, ValueError) as exc:
        if debug:
            print("YouTube request failed:", exc)
        return "Reflex: Incorrect link!"

    parser = _VideoTitleParser()
    parser.feed(page)
    parser.close()

    if parser.title:
        result = unescape(parser.title)
    else:
        result = "No title for video, could be removed / does not exist at all"

    if cache_path is not None:
        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with cache_path.open("wb") as cache_file:
                pickle.dump([result, time.time()], cache_file)
        except (OSError, pickle.PicklingError) as exc:
            if debug:
                print("YouTube cache write failed:", exc)

    return result