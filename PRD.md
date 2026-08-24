# Stock Price Fetcher — PRD

## Overview
Build a CLI tool and local website that lets you fetch current stock prices for a list of ticker symbols, save them to a CSV file, and view them in a simple HTML table.

## User
You — a finance professional who wants to quickly pull down stock prices and visualize them locally without logging into a brokerage or financial website.

## Inputs
- **CLI input**: A list of stock ticker symbols passed as command-line arguments (e.g., `python fetch.py AAPL MSFT TSLA`)
- **Data source**: Real stock prices from yfinance (free, no API key required)

## Outputs
1. **CSV file**: A file named `prices.csv` in the same directory with columns: `Ticker`, `Price` (rounded to 2 decimals), `Timestamp` (ISO 8601 format, e.g., `2026-08-24T14:30:00`)
2. **Local HTML page**: A single `index.html` file you can open in a browser that displays the latest data in a clean table. The HTML file contains the price data embedded as plain HTML (no runtime file reading, no JavaScript)

## Success Criteria
- [x] CLI tool accepts ticker symbols as arguments
- [x] Fetches real prices from a public API
- [x] Saves data to `prices.csv` with correct columns
- [x] Generates an `index.html` file that displays the data
- [x] Website works when opened locally (no server required, pure HTML/CSS)
- [x] Completes successfully with at least 3 ticker symbols

## Out of Scope
- **Real-time updates or polling** — one-shot fetch only
- **Charting or graphs** — table display only
- **Historical data or price movement** — current price only
- **Authentication** — use free API with no key required or freely available key
- **Error handling beyond basic** — if a ticker is invalid, skip it and print a message to stdout
- **Hosting or deployment** — local files only
- **User input via the website** — ticker list via CLI only
- **Dark mode, responsive design, or fancy CSS** — bare-bones table is fine
- **Database or persistence** — each run overwrites the CSV

## Constraints
- Python 3.8+
- Use yfinance library (free, no paid APIs)
- Single Python script named `fetch.py` — running it generates both `prices.csv` and `index.html` in the same directory
- Website is a single `index.html` file with embedded data (no build step, no runtime file reading)

---

**Done when**: You can run the CLI, get a CSV file and an HTML page, open the HTML in your browser, and see a table with real stock prices.
