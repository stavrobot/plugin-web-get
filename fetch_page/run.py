#!/usr/bin/env -S uv run
# /// script
# dependencies = ["curl_cffi", "beautifulsoup4"]
# ///

import json
import sys
import uuid
from pathlib import Path


def main() -> None:
    """Fetch a web page and write its content to a temp file, returning the filename and final URL."""
    params = json.load(sys.stdin)
    url = params["url"]
    # The manifest schema doesn't support defaults, so we handle the default here.
    strip_html = params.get("strip_html", True)

    from curl_cffi import requests
    from bs4 import BeautifulSoup

    response = requests.get(
        url,
        timeout=20,
        impersonate="chrome",
    )
    response.raise_for_status()

    # 24MB leaves a safe margin under the 25MB transport limit.
    if len(response.text.encode("utf-8")) > 24 * 1024 * 1024:
        print(f"Response from {url} exceeds 24MB limit, aborting.", file=sys.stderr)
        sys.exit(1)

    output_dir = Path("/tmp/web-get")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_id = uuid.uuid4().hex

    if strip_html:
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.get_text(separator="\n", strip=True)
        filename = f"{file_id}.txt"
        (output_dir / filename).write_text(content, encoding="utf-8")
    else:
        filename = f"{file_id}.html"
        (output_dir / filename).write_text(response.text, encoding="utf-8")

    json.dump({"file": filename, "url": response.url}, sys.stdout)


main()
