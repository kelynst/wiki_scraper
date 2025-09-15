import csv
import time
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# You can change this to any Wikipedia category URL you like:
# e.g., "https://en.wikipedia.org/wiki/Category:American_singers"
BASE_CATEGORY_URL = "https://en.wikipedia.org/wiki/Category:Data_science"

USER_AGENT = "KelynPracticeScraper/1.0 (+mailto:youremail@example.com)"
DELAY_SECONDS = 1.0     # polite delay between requests
LIMIT = 100             # max rows to collect (0 = no limit)

def fetch(url: str) -> str:
    """Download HTML from the given URL."""
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=20)
    r.raise_for_status()
    return r.text

def parse_category_page(html: str):
    """
    Parse one category page. Return (rows, next_page_url)
    rows: list of {"title": ..., "url": ...}
    next_page_url: absolute URL for 'next page' or None
    """
    soup = BeautifulSoup(html, "lxml")

    # The category members live under #mw-pages as list items
    rows = []
    members_root = soup.select_one("div#mw-pages")
    if members_root:
        for a in members_root.select("li > a"):
            title = a.get_text(strip=True)
            href = a.get("href")
            if not href:
                continue
            full_url = urljoin("https://en.wikipedia.org/", href)
            rows.append({"title": title, "url": full_url})

    # Find the 'next page' link (if present)
    next_page_url = None
    # Links in the nav area often include 'next page' text or a 'pagefrom' parameter
    for a in members_root.select("a") if members_root else []:
        text = a.get_text(strip=True).lower()
        href = a.get("href") or ""
        if text == "next page" or re.search(r"[?&]pagefrom=", href):
            next_page_url = urljoin("https://en.wikipedia.org/", href)
            break

    return rows, next_page_url

def main():
    url = BASE_CATEGORY_URL
    count = 0

    with open("wikipedia_category.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url"])
        writer.writeheader()

        while url:
            html = fetch(url)
            rows, url = parse_category_page(html)

            for row in rows:
                writer.writerow(row)
                count += 1
                if LIMIT and count >= LIMIT:
                    url = None
                    break

            time.sleep(DELAY_SECONDS)

    print(f"Done. Wrote {count} rows to wikipedia_category.csv")

if __name__ == "__main__":
    main()