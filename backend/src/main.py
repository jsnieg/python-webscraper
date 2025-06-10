# Requirements
# - python 3.12
# - beautifulsoup4
# - colorama
# - django

# Libraries
import asyncio
import django
import urllib.parse
import requests
import re
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from colorama import init as colorama_init
from colorama import Fore, Style

unavailable_version: str = "VERSION UNAVAILABLE"

#async def main() -> None:
#    pass

# TODO;
# - scrape first 'n' number of movies visible

def main() -> None:
    print(f'Initialising colorama to give console text color')
    colorama_init()
    print('Initialised.')

    data: list = []
    # URL: str = 'https://letterboxd.com/films/popular/upcoming/'
    URL: str = 'https://letterboxd.com/films/ajax/popular/upcoming/?esiAllowFilters=true'
    print(f"Sending a get request to URL {Fore.BLUE}[{URL}]{Style.RESET_ALL}")
    soup = BeautifulSoup(
        requests.get(url=URL).text,
        features="html.parser", # gets rid of warning
    )
    # print(f'What a Beautiful Soup!')
    # print(soup)
    for lbx in soup.select('li.listitem'):
        data.append({
            'title': lbx.img.get('alt'),
            'image_src': lbx.img.get('src'),
            'image_srcset': lbx.img.get('srcset'),
        })
    print(data)
    
    # found = soup.find_all("li", class_="listitem poster-container")
    # print(found)

if __name__ == "__main__":
    main()
    # asyncio.run(main())