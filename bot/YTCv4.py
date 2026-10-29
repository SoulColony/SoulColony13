import pickle
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import URLError
from urllib.parse import parse_qs, urlsplit
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
        content = attributes.get("content")
        if content is None:
            return

        name = attributes.get("name", "").lower()
        property_name = attributes.get("property", "").lower()

        if name == "title":
            self.title = content
        elif property_name == "og:title" and self.title is None:
            self.title = content


def YTCV4(youtube_url, cache=1, debug=0):
    """Fetch a video title; cache is retained as a legacy argument."""
    if not isinstance(youtube_url, str):
        return "Reflex: Incorrect link!"

    youtube_url = youtube_url.strip()
    youtube_url = youtube_url.replace("http//", "http://", 1)

    if youtube_url.lower().startswith("www."):
        youtube_url = "https://" + youtube_url

    try:
        parsed_url = urlsplit(youtube_url)
        if parsed_url.scheme.lower() not in ("http", "https"):
            return "Reflex: Incorrect link start"

        host = (parsed_url.hostname or "").lower()
        if host not in (
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
            "youtu.be",
            "www.youtu.be",
        ):
            return "Reflex: Incorrect link!"

        if host in ("youtu.be", "www.youtu.be"):
            video_id = parsed_url.path.strip("/").split("/")[0]
        else:
            video_id = parse_qs(parsed_url.query).get("v", [""])[0]
    except ValueError:
        return "Reflex: Incorrect link!"

    if not video_id:
        return "Reflex: Where's the watch?v=?"

    if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id) is None:
        return "Reflex: Video cannot exist"

    first_two = video_id[:2]
    if no_absolute_paths:
        cache_dir = Path("YTCache")
    else:
        cache_dir = Path(directory) / "YTCache"

    cache_path = cache_dir / (first_two + ".tcc")
    prev_dict = {}

    try:
        with cache_path.open("rb") as cache_file:
            loaded_cache = pickle.load(cache_file, encoding="latin1")

        if isinstance(loaded_cache, dict):
            prev_dict = loaded_cache
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

    cached_title = prev_dict.get(video_id)
    if isinstance(cached_title, str):
        return cached_title

    request_url = "https://www.youtube.com/watch?v=" + video_id

    try:
        with urlopen(request_url, timeout=15) as website:
            encoding = website.headers.get_content_charset() or "utf-8"
            page = website.read().decode(encoding, errors="replace")
    except (URLError, OSError, ValueError) as exc:
        if debug:
            print("YouTube request failed:", exc)
        return "Reflex: Incorrect link!"

    parser = _VideoTitleParser()
    parser.feed(page)
    parser.close()

    if not parser.title:
        return (
            "No title for video, Removed / Needs age verification / "
            "Does not exist"
        )

    result = parser.title
    prev_dict[video_id] = result

    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        with cache_path.open("wb") as cache_file:
            pickle.dump(prev_dict, cache_file)
    except (OSError, pickle.PicklingError) as exc:
        if debug:
            print("YouTube cache write failed:", exc)

    return result