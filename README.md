# Court-Data Fetcher & Mini-Dashboard

A Python Flask app to fetch and display Delhi High Court case details (parties, filing/next-hearing date, order PDFs) by case type/number/year.

## Court Chosen

Delhi High Court — https://delhihighcourt.nic.in/

## Stack

- Python 3.x
- Flask (Backend, UI)
- Playwright (Web scraping)
- SQLite (Logging queries/raw HTML)
- BeautifulSoup (Parsing)

## Install & Run

1. Clone repo:  
   `git clone <your_repo_url>`
   
2. Install dependencies:  
   `pip install -r requirements.txt`  
   Then:  
   `playwright install`
   
3. Start app:  
   `python app.py`
   
4. Open [http://localhost:5000](http://localhost:5000)

## CAPTCHA/Token Handling

If a CAPTCHA appears, the app pauses for manual intervention (screenshot saved as `captcha.png`).  
**Document in the readme**: If persistent and not bypassable, describe exactly what you tried; for partial credit submit screenshots, code, and clearly document blocker.

## Features

- Simple 3-field HTML form.
- Scrapes case data, parses and displays key info.
- Shows latest order/judgment PDF link if available.
- Logs each query and raw HTML in SQLite.
- Graceful error display for invalid input/site issues.

## Optional

- To run with Docker:  
  *(Add a simple Dockerfile if needed.)*

## Environment Variables

- (e.g., Flask secret, if made configurable.)

## Demo Video

See demo.mp4 or YouTube link.

## Licence

MIT

## Credits

Playwright, Flask, BeautifulSoup, Delhi High Court Portal.
