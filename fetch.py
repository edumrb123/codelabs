#!/usr/bin/env python3
"""
Stock Price Fetcher — CLI tool to fetch current stock prices and generate CSV + HTML outputs.
Usage: python fetch.py AAPL MSFT TSLA
"""

import sys
import csv
from datetime import datetime
import yfinance as yf


def fetch_stock_price(ticker):
    """
    Fetch the current price for a given ticker symbol.
    Returns a dict with 'ticker', 'price', and 'timestamp' on success.
    Returns None if the ticker is invalid or the fetch fails.
    """
    try:
        stock = yf.Ticker(ticker)
        # Fetch the most recent price
        data = stock.history(period="1d")
        if data.empty:
            print(f"INVALID: {ticker} not found")
            return None
        # Get the closing price from the latest row
        price = data['Close'].iloc[-1]
        if price is None or price != price:  # Check for NaN
            print(f"INVALID: {ticker} not found")
            return None
        return {
            'ticker': ticker.upper(),
            'price': round(float(price), 2),
            'timestamp': datetime.now().isoformat(timespec='seconds')
        }
    except Exception as e:
        print(f"INVALID: {ticker} not found")
        return None


def generate_html(data):
    """
    Generate an HTML string with embedded price data in a table.
    """
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Stock Prices</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            max-width: 600px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        h1 {
            color: #333;
        }
    </style>
</head>
<body>
    <h1>Stock Prices</h1>
    <table>
        <tr>
            <th>Ticker</th>
            <th>Price</th>
            <th>Timestamp</th>
        </tr>
"""

    for row in data:
        html += f"""        <tr>
            <td>{row['ticker']}</td>
            <td>${row['price']:.2f}</td>
            <td>{row['timestamp']}</td>
        </tr>
"""

    html += """    </table>
</body>
</html>
"""
    return html


def main():
    """Main function to orchestrate fetching, CSV writing, and HTML generation."""
    if len(sys.argv) < 2:
        print("Usage: python fetch.py AAPL MSFT TSLA")
        sys.exit(1)

    tickers = sys.argv[1:]
    data = []

    # Fetch prices for each ticker
    print(f"Fetching prices for {len(tickers)} ticker(s)...")
    for ticker in tickers:
        result = fetch_stock_price(ticker)
        if result:
            data.append(result)

    if not data:
        print("No valid tickers provided.")
        sys.exit(1)

    # Write to CSV
    csv_filename = "prices.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Ticker', 'Price', 'Timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({
                'Ticker': row['ticker'],
                'Price': row['price'],
                'Timestamp': row['timestamp']
            })
    print(f"Saved {len(data)} prices to {csv_filename}")

    # Generate and write HTML
    html_filename = "index.html"
    html_content = generate_html(data)
    with open(html_filename, 'w') as htmlfile:
        htmlfile.write(html_content)
    print(f"Generated {html_filename}")


if __name__ == "__main__":
    main()

# >>> BUILDER COMPLETE. Handing off to PR-OPENER.
