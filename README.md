# 🕷️ wiki_scraper  

Python web scraper using **Requests** + **BeautifulSoup** to extract structured data from any Wikipedia category and export it into clean CSV files.  

---

## 📌 Features  
- Scrapes **titles + URLs** from Wikipedia categories  
- Follows **pagination** (collects across multiple pages)  
- Customizable from the terminal with:  
  - `--url` → which category to scrape  
  - `--limit` → how many rows to collect  
  - `--delay` → how many seconds to wait between requests  
  - `--out` → output CSV filename  

---

## 📦 Installation  

Clone the repo and set up your environment:  

```bash
git clone https://github.com/kelynst/wiki_scraper.git
cd wiki_scraper
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows PowerShell
pip install -r requirements.txt
```

---

## ▶️ Usage  

### Default run (scrapes the Phobias category, saves 100 rows max):  
```bash
python scrape_wiki.py
```

### Example: scrape Horror movies, limit to 50 rows, custom output file:  
```bash
python scrape_wiki.py --url "https://en.wikipedia.org/wiki/Category:Horror_films" --limit 50 --out horror_movies.csv
```

### Example: scrape Vacation destinations with a 0.5s delay between requests:  
```bash
python scrape_wiki.py --url "https://en.wikipedia.org/wiki/Category:Tourist_attractions" --limit 200 --delay 0.5 --out vacation_spots.csv
```

---

## 📝 Example Output  

`phobias.csv`  

```
title,url
Acrophobia,https://en.wikipedia.org/wiki/Acrophobia
Claustrophobia,https://en.wikipedia.org/wiki/Claustrophobia
Nyctophobia,https://en.wikipedia.org/wiki/Nyctophobia
Ophidiophobia,https://en.wikipedia.org/wiki/Ophidiophobia
...
```

---

## ⚠️ Notes  

- Wikipedia scraping is allowed for personal/educational use. Always be respectful with delays so you don’t overload their servers.  
- Output CSV files (`*.csv`) are ignored in this repo (see `.gitignore`).  

---