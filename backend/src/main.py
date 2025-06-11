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
from bs4 import BeautifulSoup, Tag
from playwright.async_api import async_playwright
from colorama import init as colorama_init
from colorama import Fore, Style

unavailable_version: str = "VERSION UNAVAILABLE"

#async def main() -> None:
#    pass

# TODO;
# - scrape first 'n' number of movies visible
# - classes (oop)

def timestamp_of_now():
    """Method for calling timestamp of now."""
    return datetime.datetime.now()

def scrape_page(urls: list[str]=None, URL: str="") -> BeautifulSoup:
    """Method for scraping a list of URL pages/URL."""
    soup = None
    print(f"[{timestamp_of_now()}] Sending a get request to URL\n{Fore.BLUE}[{URL}]{Style.RESET_ALL}")
    print(f'[{timestamp_of_now()}] {Fore.GREEN}Scraping the webpage...{Style.RESET_ALL}')
    if urls is not None:
        return
    else:
        soup = BeautifulSoup(
            markup=requests.get(url=URL).text,
            features="html.parser", # gets rid of warning
        )
    return soup

def scrape_movie_information(soup: BeautifulSoup) -> list[dict]:
    """Method for scraping basic information about the movies e.g., titles and img URL"""
    data: list[dict] = []
    number_of_movies: int = None

    print(f"[{timestamp_of_now()}] {Fore.GREEN}Scraping contents...{Style.RESET_ALL}")
    for lbx in soup.select('p.ui-block-heading'):
        # Remove all whitespaces in the <p></p>
        text: str = lbx.get_text().strip()

        # Find all numbers within the string using regex
        text: list = re.findall(r'\b\d+\b', text)

        # Join string together and cast to int
        number_of_movies: int = int(''.join(text))
    print(f'\t{Fore.RED}*{Style.RESET_ALL}There are [{number_of_movies}] movies in total.')

    individual_movies_count: int = 0
    # Return all movie information
    for lbx in soup.select('li.listitem'):
        individual_movies_count += 1
        data.append({
            'title': lbx.img.get('alt'),
            'image_src': lbx.img.get('src'),
            'image_srcset': lbx.img.get('srcset'),
        })

    print(f'\t{Fore.RED}*{Style.RESET_ALL}There are [{individual_movies_count}] movies on this page.')
    print(f'\t{Fore.RED}*{Style.RESET_ALL}There are potentially ~[{number_of_movies // individual_movies_count}] movies in this category.')
    return data

def get_url_of_container(soup: BeautifulSoup) -> str | list[str]:
    """Method for finding a url of the container to scrape."""
    try:
        print(f"[{timestamp_of_now()}] Scraping to get [data-url] of the film's container")
        container: Tag = soup.find('div', {'id': 'films-browser-list-container'})
        url_found: str | list[str] = container['data-url']
        if url_found:
            print(f"[{timestamp_of_now()}] URL found!\n{Fore.BLUE}[{url_found}]{Style.RESET_ALL}")
            return url_found
        else:
            print(f"[{timestamp_of_now()}]{Fore.RED}URL was not found!{Style.RESET_ALL}")
            return
    except Exception as _exception:
        print(_exception)

def main() -> None:
    colorama_init()
    URL: str = "https://letterboxd.com"
    PATH: str = "/films/popular/decade/2020s/"
    web_soup: BeautifulSoup = scrape_page(URL=URL+PATH)
    container_url: BeautifulSoup = get_url_of_container(web_soup)
    container_soup: BeautifulSoup = scrape_page(URL=URL+container_url)
    scrape_movie_information(container_soup)

##########################    
if __name__ == "__main__":
    main()
    # asyncio.run(main())