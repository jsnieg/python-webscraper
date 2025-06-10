# Requirements
# - python 3.12
# - beautifulsoup
# - colorama
# - django

# Libraries
import asyncio
import django
import urllib.parse
import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from colorama import init as colorama_init
from colorama import Fore, Style

unavailable_version: str = "VERSION UNAVAILABLE"

#async def main() -> None:
#    pass

def main() -> None:
    print(f'Initialising colorama to give console text color')
    colorama_init()
    print('Initialised.')

    data: list = []
    URL: str = 'https://letterboxd.com/films/popular/upcoming/'
    print(f"Sending a get request to URL {Fore.BLUE}[{URL}]{Style.RESET_ALL}")
    soup = BeautifulSoup(
        requests.get(url=URL).text,
        features="html.parser" # gets rid of warning
    )
    print(f'What a Beautiful Soup!')
    # print(soup)
    for lbx in soup.select('li.listitem'):
        data.append({
            'title': lbx.img.get('alt'),
        })
    print(data)

if __name__ == "__main__":
    main()
    # asyncio.run(main())