"""Fetch HTML page titles for IRC link previews."""
import ipaddress
import socket
from html.parser import HTMLParser
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


MAX_BYTES = 262144


class _TitleParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.finished = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title" and not self.finished:
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title" and self.in_title:
            self.in_title = False
            self.finished = True

    def handle_data(self, data):
        if self.in_title:
            self.parts.append(data)


def _validate_url(url):
    parsed = urlsplit(url)
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("Only HTTP and HTTPS links are supported")
    if not parsed.hostname or parsed.username is not None or parsed.password is not None:
        raise ValueError("Invalid link or embedded credentials")
    port = parsed.port or (443 if parsed.scheme.lower() == "https" else 80)
    if port not in (80, 443):
        raise ValueError("Nonstandard web ports are not supported")
    addresses = socket.getaddrinfo(parsed.hostname, port, type=socket.SOCK_STREAM)
    if not addresses or any(
        not ipaddress.ip_address(address[4][0]).is_global
        for address in addresses
    ):
        raise ValueError("Nonpublic network addresses are not supported")


class _CheckedRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def TitleCheck(link):
    """Return a single-line title, or an empty string on failure."""
    try:
        if not isinstance(link, str):
            return ""
        link = link.strip()
        _validate_url(link)
        request = Request(link, headers={"User-Agent": "SoulColony-LinkPreview/1.0"})
        opener = build_opener(_CheckedRedirects())
        with opener.open(request, timeout=10) as response:
            if response.headers.get_content_type() not in (
                "text/html", "application/xhtml+xml",
            ):
                return ""
            raw = response.read(MAX_BYTES)
            encoding = response.headers.get_content_charset() or "utf-8"
        try:
            text = raw.decode(encoding, errors="replace")
        except LookupError:
            text = raw.decode("utf-8", errors="replace")
        parser = _TitleParser()
        parser.feed(text)
        parser.close()
        title = "".join(parser.parts)
        title = "".join(character if character.isprintable() else " " for character in title)
        return " ".join(title.split())[:250]
    except (OSError, ValueError, TypeError, HTTPError):
        return ""
