import csv
import time
import re
import argparse
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Default category (change if you want; or pass --url at runtime)
DEFAULT_URL = "https://en.wikipedia.org/wiki/Category:Phobias"

# Polite, professional User-Agent (no personal email needed)
USER_AGENT = "KelynWikipediaScraper/1.1 (+https://github.com/kelynst/wiki_scraper)"

def fetch(url: str, timeout: int = 20) -> str:
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    r.raise_for_status()
    return r.text

def parse_category_page(html: str):
    """
    Return (rows, next_page_url).
    rows: list of {'title': ..., 'url': ...}
    next_page_url: absolute URL to the next page, or None if no more pages.
    """
    soup = BeautifulSoup(html, "lxml")

    rows = []
    members_root = soup.select_one("div#mw-pages")  # category listings live here
    if members_root:
        # Each article appears as <li><a href="/wiki/...">Title</a></li>
        for a in members_root.select("li > a"):
            title = a.get_text(strip=True)
            href = a.get("href")
            if not href:
                continue
            full_url = urljoin("https://en.wikipedia.org/", href)
            rows.append({"title": title, "url": full_url})

    # Look for pagination ("next page") link
    next_page_url = None
    for a in members_root.select("a") if members_root else []:
        text = a.get_text(strip=True).lower()
        href = a.get("href") or ""
        if text == "next page" or re.search(r"[?&]pagefrom=", href):
            next_page_url = urljoin("https://en.wikipedia.org/", href)
            break

    return rows, next_page_url

def main():
    parser = argparse.ArgumentParser(description="Scrape a Wikipedia category into CSV.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Wikipedia category URL")
    parser.add_argument("--limit", type=int, default=100, help="Max rows to collect (0 = unlimited)")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds to sleep between page requests")
    parser.add_argument("--out", default="wikipedia_category.csv", help="Output CSV filename")
    args = parser.parse_args()

    url = args.url
    limit = max(0, args.limit)
    delay = max(0.0, args.delay)
    out_path = args.out

    count = 0
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url"])
        writer.writeheader()

        while url:
            print(f"Fetching: {url}")
            html = fetch(url)
            rows, url = parse_category_page(html)
            print(f"Got {len(rows)} rows from this page")

            for row in rows:
                writer.writerow(row)
                count += 1
                if limit and count >= limit:
                    url = None
                    break

            if url:
                time.sleep(delay)

    print(f"Done. Wrote {count} rows to {out_path}")

if __name__ == "__main__":
    main()
