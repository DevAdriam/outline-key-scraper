# Outline Key Scraper and Validator

This project is a Python script that scrapes keys from the `outlinekeys.com` website and checks their validity using a validation endpoint. The script uses BeautifulSoup for HTML parsing and the `requests` library to fetch the web pages and perform key validation.

## Features

- Scrapes key details from the `outlinekeys.com` website.
- Validates each key using an API endpoint.
- Returns a list of valid keys in an array.
- Handles network errors and missing elements gracefully.

## Requirements

- Python 3.9 or higher
- `requests` library
- `BeautifulSoup4` library
- `lxml` parser

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DevAdriam/Outline-Key-Scraper.git
   cd outline-key-scraper
   ```

2. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. Run:
   ```bash
    python main.py
   ```
