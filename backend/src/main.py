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
import datetime
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from colorama import init as colorama_init
from colorama import Fore, Style

unavailable_version: str = "VERSION UNAVAILABLE"

#async def main() -> None:
#    pass

# TODO;
# - scrape first 'n' number of movies visible
# - classes (oop)

def scrape_page(urls: list[str]=None, URL: str="") -> BeautifulSoup:
    """Method for scraping a list of URL pages/URL."""
    _datetime: datetime = datetime.datetime.now()
    print(f"[{_datetime}] Sending a get request to URL {Fore.BLUE}[{URL}]{Style.RESET_ALL}")
    print(f'[{_datetime}] {Fore.GREEN}Scraping movie general information...{Style.RESET_ALL}')
    soup = BeautifulSoup(
        markup=requests.get(url=URL).text,
        features="html.parser", # gets rid of warning
    )
    return soup

def scrape_movie_information(soup: BeautifulSoup) -> list[dict]:
    """Method for scraping basic information about the movies e.g., titles and img URL"""
    data: list[dict] = []
    _datetime: datetime = datetime.datetime.now()
    number_of_movies: int = None

    print(f"[{_datetime}] {Fore.GREEN}Scraping...{Style.RESET_ALL}")
    for lbx in soup.select('p.ui-block-heading'):
        # Remove all whitespaces in the <p></p>
        text: str = lbx.get_text().strip()

        # Find all numbers within the string using regex
        text: list = re.findall(r'\b\d+\b', text)

        # Join string together and cast to int
        number_of_movies: int = int(''.join(text))
    print(f'There are [{number_of_movies}] movies in total.')

    for lbx in soup.select('li.listitem'):
        data.append({
            'title': lbx.img.get('alt'),
            'image_src': lbx.img.get('src'),
            'image_srcset': lbx.img.get('srcset'),
        })

    return data

def main() -> None:
    colorama_init()
    URL: str = 'https://letterboxd.com/films/ajax/popular/upcoming/?esiAllowFilters=true'
    soup: BeautifulSoup = scrape_page(URL=URL)
    data: list[dict] = scrape_movie_information(soup)
    print(data)

if __name__ == "__main__":
    main()
    # asyncio.run(main())