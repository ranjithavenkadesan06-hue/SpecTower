
import csv
import hashlib
import os
import sys
import time
from datetime import date
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests

RAW = "data/raw"
MANIFEST = "data/manifest.csv"
USER_AGENT = "SpecTowerStudentProject/1.0"
HEADERS = {"User-Agent": USER_AGENT}
DELAY = 2

robots = {}


def allowed(url):
    parsed = urlparse(url)
    root = f"{parsed.scheme}://{parsed.netloc}"

    if root not in robots:
        rp = RobotFileParser()
        rp.set_url(root + "/robots.txt")

        try:
            rp.read()
            robots[root] = rp
        except Exception:
            # Fail closed if robots.txt cannot be checked.
            robots[root] = None

    rp = robots[root]

    # Do not download if permission cannot be verified.
    if rp is None:
        return False

    return rp.can_fetch(USER_AGENT, url)


def name_for(url):
    name = os.path.basename(urlparse(url).path) or "index.html"
    return name.replace(" ", "_")


def main(list_file):
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)

    new_manifest = not os.path.exists(MANIFEST)

    with open(MANIFEST, "a", newline="", encoding="utf-8") as mf:
        log = csv.writer(mf)

        if new_manifest:
            log.writerow(
                ["file", "source_url", "downloaded_on", "bytes", "sha256"]
            )

        with open(list_file, encoding="utf-8") as fh:
            urls = [line.strip() for line in fh]

        with requests.Session() as session:
            session.headers.update(HEADERS)

            for url in urls:
                if not url or url.startswith("#"):
                    continue

                path = os.path.join(RAW, name_for(url))

                if os.path.exists(path):
                    print("skip (already have)", path)
                    continue

                if not allowed(url):
                    print("not downloaded; robots permission unavailable:", url)
                    continue

                try:
                    response = session.get(url, timeout=30)
                    response.raise_for_status()
                except requests.RequestException as exc:
                    print("download failed:", url, exc)
                    continue

                content = response.content
                digest = hashlib.sha256(content).hexdigest()

                with open(path, "wb") as output:
                    output.write(content)

                log.writerow(
                    [
                        path.replace("\\", "/"),
                        url,
                        date.today().isoformat(),
                        len(content),
                        digest,
                    ]
                )
                mf.flush()

                print("saved", path, len(content), "bytes")
                time.sleep(DELAY)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/download.py urls.txt")
        sys.exit(1)

    main(sys.argv[1])
