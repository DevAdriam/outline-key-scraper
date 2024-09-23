from bs4 import BeautifulSoup
from colorama import Fore, Style, init

import requests
import sys
import urllib3


# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

outline_key_url = "https://outlinekeys.com"

try:
    outline_key_html = requests.get(outline_key_url, verify=False).text
except requests.exceptions.RequestException as e:
    print(f"Error fetching {outline_key_url}: {e}", file=sys.stderr)
    sys.exit(1)

soup = BeautifulSoup(outline_key_html, 'lxml')
key_link = soup.find_all("a", class_="row g-0 text-decoration-none")


def is_key_valid(key):
    validation_url = "https://outlinekeys.com/validate"

    payload = {
        'key': key
    }

    try:
        response = requests.post(validation_url, data=payload, verify=False)

        if response.status_code == 200:
            result = response.json()
            if result.get('valid'):
                print(f"valid key : {Fore.GREEN}{key}")
                return True
        return False

    except requests.exceptions.RequestException as e:
        print(f"Error validating key {Fore.RED}{key}{Style.RESET_ALL}: {e}")
        return False


for key in key_link:
    href = key.get("href")

    if href:
        detail_url = outline_key_url + href
        try:
            outline_key_detail_html = requests.get(
                detail_url, verify=False).text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {detail_url}: {e}", file=sys.stderr)
            continue

        detail_soup = BeautifulSoup(outline_key_detail_html, 'lxml')
        get_key = detail_soup.find(
            "textarea", class_="form-control shadow-none")

        if get_key:
            is_key_valid(get_key.text.strip())
        else:
            print(f"No key found on page: {detail_url}")
    else:
        print("No href found for key link, skipping.")
