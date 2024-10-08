from bs4 import BeautifulSoup
from colorama import Fore, Style, init

import requests
import subprocess
import sys
import urllib3
import pyautogui
import time

# Initialize colorama for terminal coloring
init(autoreset=True)

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

OUTLINE_KEY_URL = "https://outlinekeys.com"
PLUS_BUTTON_IMG = 'assests/plus_button.jpeg'
INVALID_KEY_IMG = 'assests/invalid_key.jpeg'
OUTLINE_CLIENT_PATH ="/Applications/Outline.app/Contents/MacOS/Outline"


def fetch_outline_keys(url):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error fetching {url}: {e}", file=sys.stderr)
        sys.exit(1)


def extract_keys_from_html(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    key_links = soup.find_all("a", class_="row g-0 text-decoration-none")
    return key_links


def fetch_key_detail(detail_url):
    try:
        detail_html = requests.get(detail_url, verify=False).text
        detail_soup = BeautifulSoup(detail_html, 'lxml')
        key_element = detail_soup.find("textarea", class_="form-control shadow-none")
        return key_element.text.strip() if key_element else None
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error fetching {detail_url}: {e}", file=sys.stderr)
        return None


def open_outline_app():
    subprocess.Popen(['open', OUTLINE_CLIENT_PATH])
    time.sleep(3)  #


def test_outline_key(outline_key):
    plus_button_location = pyautogui.locateOnScreen(PLUS_BUTTON_IMG, confidence=0.8)
    if plus_button_location:
        center_x, center_y = pyautogui.center(plus_button_location)
        print(f"{Fore.GREEN}Plus button found at: {plus_button_location}")

        pyautogui.moveTo((center_x / 2), (center_y / 2), duration=0.3)
        time.sleep(0.3)
        pyautogui.click()
        time.sleep(0.5)

        pyautogui.moveTo((center_x / 2) - 200,(center_y / 2) + 340, duration=0.3)
        pyautogui.click()
        pyautogui.typewrite(outline_key)
        time.sleep(0.8)

        pyautogui.moveTo((center_x / 2) - 60,(center_y / 2) + 420,duration=0.3)
        time.sleep(0.3)
        pyautogui.click()
        time.sleep(1)


        pyautogui.moveTo((center_x / 2), (center_y / 2)+100, duration=0.3)
        pyautogui.click()
        time.sleep(1)

    else:
        print(f"{Fore.RED}Plus button not found.")


def main():
    outline_key_html = fetch_outline_keys(OUTLINE_KEY_URL)

    key_links = extract_keys_from_html(outline_key_html)

    open_outline_app()

    for key in key_links:
        href = key.get("href")
        if href:
            detail_url = OUTLINE_KEY_URL + href
            outline_key = fetch_key_detail(detail_url)

            if outline_key:
                print(f"{Fore.CYAN}Testing key: {outline_key}")
                test_outline_key(outline_key)
            else:
                print(f"{Fore.YELLOW}No key found on page: {detail_url}")
        else:
            print(f"{Fore.YELLOW}No href found for key link, skipping.")


if __name__ == "__main__":
    main()
