from pathlib import Path


directory = ""


def percentage(value, total):
    return round(value / total * 100, 1) if total else 0.0


def main():
    root = Path(directory or ".")
    files = sorted(
        path for path in root.iterdir()
        if path.is_file() and path.suffix == ".py"
    )
    print(len(files), "Files")
    records = []

    for path in files:
        with path.open("r", encoding="utf-8", errors="replace") as source:
            text = source.read()

        # Match text-file iteration: only newline characters end lines.
        line_count = text.count("\n")
        if text and not text.endswith("\n"):
            line_count += 1

        records.append((line_count, len(text), path.name, path.stat().st_size))

    total_lines = sum(record[0] for record in records)
    total_letters = sum(record[1] for record in records)
    total_bytes = sum(record[3] for record in records)

    print(total_lines, "Lines in total")
    print(total_letters, "Letters in total")
    print(total_bytes, "Bytes in total")

    for line_count, letter_count, filename, byte_count in records:
        print(
            f"{line_count} Lines ({percentage(line_count, total_lines)}%) || "
            f"{letter_count} Letters "
            f"({percentage(letter_count, total_letters)}%) in file {filename}"
        )
        print(f"{byte_count} Bytes ({percentage(byte_count, total_bytes)}%)")


if __name__ == "__main__":
    main()