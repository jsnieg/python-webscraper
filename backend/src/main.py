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
from colorama import init as colorama_init
from colorama import Fore, Style
from dataclasses import dataclass

unavailable_version: str = "VERSION UNAVAILABLE"

#async def main() -> None:
#    pass

# TODO;
# - scrape first 'n' number of movies visible
# - classes (oop)

@dataclass
class WebScraper():
    # def __init__(self, urls: list[str]):
    #     self.URL = urls
    urls: list[str]

    def scrape_page(self, urls: list[str]) -> BeautifulSoup | None:
        self.urls = urls

def scrape_page(urls: list[str] | str=None) -> BeautifulSoup | None:
    """Method for scraping a list of URL pages/URL."""
    soup = None
    print(f"[{datetime.datetime.now()}] Sending a get request to URL(s)\n\t{Fore.BLUE}[{urls}]{Style.RESET_ALL}")
    print(f'[{datetime.datetime.now()}] {Fore.GREEN}Scraping the webpage...{Style.RESET_ALL}')
    if urls == type(str) or urls != "":
        try:
            http_request: requests.Response = requests.get(url=urls)
            print(f'\t{Fore.RED}*{Style.RESET_ALL}Response {http_request.status_code}')
            if http_request.status_code == 200:
                soup = BeautifulSoup(
                    markup=http_request.text,
                    features="html.parser", # gets rid of warning
                )
                return soup
            else:
                print(f"[{datetime.datetime.now()}]{Fore.RED} Bad GET Request, failed to trigger HTTP request.{Style.RESET_ALL}")
                return
        except Exception as _exception:
            print(_exception)
            return
    else:
        print(f'\t{Fore.RED}*{Style.RESET_ALL} No specified URL.')
        return

def scrape_poster_lists(soup: BeautifulSoup) -> list[dict]:
    """Method for scraping basic information about the movie llist on the webpage not individual."""
    data: list[dict] = []
    number_of_movies: int = None
    if soup == None or soup == type(None):
        print(f"[{datetime.datetime.now()}]{Fore.RED} Failed to scrape, probable cause is bad GET request. Retry the API call or wait before attempting again.{Style.RESET_ALL}")
        return
    else:
        try:
            print(f"[{datetime.datetime.now()}] {Fore.GREEN}Scraping contents...{Style.RESET_ALL}")
            for lbx in soup.select('p.ui-block-heading'):
                # Remove all whitespaces in the <p></p>
                text: str = lbx.get_text().strip()

                # Find all numbers within the string using regex
                text: list = re.findall(r'\b\d+\b', text)
                if text:
                    # Join string together and cast to int
                    number_of_movies: int = int(''.join(text))
                else:
                    print(f'\t{Fore.RED}*{Style.RESET_ALL} No movies on this webpage.')
            print(f'\t{Fore.RED}*{Style.RESET_ALL}There are [{number_of_movies}] movies in total.')

            individual_movies_count: int = 0
            # Return all movie information
            for lbx in soup.select('li.listitem'):
                individual_movies_count += 1
                data.append({
                    'title': lbx.img.get('alt'),
                    'path': lbx.find('div')['data-film-slug'],
                    'rating': float(lbx['data-average-rating']),
                })
            
            average_rating: float = sum([d["rating"] for d in data]) / individual_movies_count

            print(f'\t{Fore.RED}*{Style.RESET_ALL}There are [{individual_movies_count}] movies on this page.')
            print(f'\t{Fore.RED}*{Style.RESET_ALL}There are potentially ~[{number_of_movies // individual_movies_count}] movies in this category.')
            print(f'\t{Fore.RED}*{Style.RESET_ALL}Average rating is [{average_rating:.2f}] in this category.')
            print(f'\t{Fore.RED}*{Style.RESET_ALL}Example URL of the movie: [https://letterboxd.com/film/{[d['path'] for d in data][0]}]')
            return data
        except Exception as _exception:
            print(_exception)
            return

def get_url_of_container(soup: BeautifulSoup) -> str | list[str]:
    """
    Method for finding a url of the container to scrape.
    
    The custom data attribute in HTML (least to my knowledge and understanding) prevents you from scraping that particular container hence we need data-url.
    """
    if soup == None or soup == type(None):
        print(f"[{datetime.datetime.now()}]{Fore.RED} Failed to scrape, probable cause is bad GET request. Retry the API call or wait before attempting again.{Style.RESET_ALL}")
        return
    try:
        print(f"[{datetime.datetime.now()}] Scraping to get [data-url] of the film's container")
        container: Tag = soup.find(name='div', attrs={'id': 'films-browser-list-container'})
        url_found: str | list[str] = container['data-url']
        if url_found:
            print(f"[{datetime.datetime.now()}] URL found!\n\t{Fore.BLUE}[{url_found}]{Style.RESET_ALL}")
            return url_found
        else:
            print(f"[{datetime.datetime.now()}]{Fore.RED} URL was not found!{Style.RESET_ALL}")
            return ""
    except Exception as _exception:
        print(f"[{datetime.datetime.now()}]{Fore.RED} URL was not found!{Style.RESET_ALL}")
        print(_exception)
        return ""
    
def scrape_movie_details(url: str = "https://letterboxd.com/film/", path: list[str] = []) -> None:
    """Scraping individual movie details e.g., description or movie poster."""
    full_url: str = url + path
    try: 
        data: BeautifulSoup = scrape_page(full_url)
        if data == None or data == type(None):
            print(f"[{datetime.datetime.now()}]{Fore.RED} Failed to scrape data is {type(data)}{Style.RESET_ALL}")
            return
        else:
            prod_synopsis = data.find('div', class_='review body-text -prose -hero prettify').find('p').get_text()
            print(prod_synopsis)
    except Exception as _exception: 
        print(f"[{datetime.datetime.now()}]{Fore.RED} Could not scrape movie details.{Style.RESET_ALL}")
        print(_exception)

def main() -> None:
    colorama_init()
    URL: str = "https://letterboxd.com"
    PATH: str = "/films/popular/decade/2020s/" # todo is be able to scrape everything...
    data: list[dict] = None
    web_soup: BeautifulSoup = scrape_page(urls=URL+PATH)
    container_url: str = get_url_of_container(web_soup)
    container_soup: BeautifulSoup = scrape_page(urls=URL+container_url)
    data=scrape_poster_lists(container_soup)
    # for dict_item in data:
    #     for key in dict_item:
    #         if key == 'path':
    #            scrape_movie_details(path=dict_item[key])
    scrape_movie_details(path=[d['path'] for d in data][0])

##########################    
if __name__ == "__main__":
    main()
    # asyncio.run(main())