from hashlib import md5
from pathlib import Path
from urllib.request import urlopen

import CORE_DATA
from FMLformatter import formatter
from save_load import save


directory = CORE_DATA.directory


def main():
    with urlopen("http://www.fmylife.com/random", timeout=15) as response:
        encoding = response.headers.get_content_charset() or "utf-8"
        page = response.read().decode(encoding, errors="replace")

    formatted = formatter(page.split("\n"))
    quote_dir = Path(directory) / "fmlquotes"
    quote_dir.mkdir(parents=True, exist_ok=True)

    for quote in formatted:
        exact = quote.partition("#")[0]
        digest = md5(
            exact.encode("utf-8"),
            usedforsecurity=False,
        ).hexdigest()
        save(str(quote_dir / (digest + ".txt")), exact)


if __name__ == "__main__":
    main()