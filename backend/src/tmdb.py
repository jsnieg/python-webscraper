import asyncio
import aiohttp
import datetime
from bs4 import BeautifulSoup, ResultSet, Tag
from colorama import init as colorama_init
from colorama import Fore, Style

from typing import Annotated
from fastapi import Body, FastAPI, Request
from pydantic import BaseModel, Field

web_url = 'https://www.themoviedb.org'

app = FastAPI()

# TODO:
# POST request for creating URL to scrape
# default on React-end: [/movie/, /movie/top-rated/, /movie/upcoming/, /movie/now-playing/]
# GET request after PUT request is called
# Authentication Demo with OAuth 2.0 [?]
# Support for scraping TV shows [?]
# Scrape more than just one page [https://www.themoviedb.org/movie/now-playing?page=2] ?page=2 is the key, could influence increment page number by 1 to 3/5. Probably 3 for testing.



class ScrapeURL(BaseModel):
    """
    A class for defining the URL as string on PUT reqeuest call.
    """
    url: str | None = Field(
        default=None,
        title="A placeholder for the URL.",
        max_length=300
    )
    # url: str | None

@app.get("/test")
async def test_api() -> dict:
    """
    Call this GET method to see if API is infact working as intended.
    """
    return {'Fast':'API'}

@app.get("/get_url")
async def get_url() -> dict:
    """
    A function that returns the set url when POST request was called.
    """
    try:
        return {'Response': app.state.url}
    except AttributeError as _exception:
        return {'Response': _exception}

@app.get("/test_fetch")
async def test_fetch() -> dict:
    try:
        url: str = str(app.state.url)
        async with aiohttp.ClientSession() as session:
            print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping main page...")
            html_page: str = await fetch(session=session, url=url)
            soup: BeautifulSoup = BeautifulSoup(
                markup=html_page,
                features='lxml'
            )
            app.state.movie_urls = await scrape_page_for_urls(soup)
            return {'Response': app.state.movie_urls}
    except Exception as _exception:
        return {'Response': _exception}

@app.post("/set_url")
# async def set_url(url: str | None, scrape_url: Annotated[ScrapeURL, Body(embed=True)]) -> str:
async def set_url(url: str, scrape_url: ScrapeURL) -> dict:
    """
    A function that sets current str for usage.

    Only acceptable URL is TMDB (https://www.themoviedb.org).
    """
    # https://stackoverflow.com/questions/71260288/how-to-share-variables-between-http-requests-in-fastapi
    app.state.url = url
    return {'Response': app.state.url}

async def fetch(session: aiohttp.ClientSession, url: str = 'https://www.themoviedb.org/movie/top-rated/') -> str:
    """
    Method for fetching webpage HTML as raw text.
    """
    print(f"[{datetime.datetime.now()}] Fetching HTML of URL: [{Fore.BLUE}{url}{Style.RESET_ALL}] w/", end=" ")
    try:
        async with session.get(url) as response:
            if response.status == 200:
                print(f"{Fore.GREEN}Response [{response.status}]{Style.RESET_ALL}")
                return await response.text()
            if response.status == 429:
                print(f"{Fore.RED}Response [{response.status}]{Style.RESET_ALL}")
            else:
                response.raise_for_status()
    except Exception as _exception:
        print(_exception)
    
async def fetch_all(session: aiohttp.ClientSession, urls: list[str]) -> list[dict]:
    """
    Method for fetching all webpages HTML(s) as raw text when a list is provided.
    """
    results: list[dict] = []
    for url in urls:
        url = web_url + url
        task: asyncio.Task = asyncio.create_task(fetch(session=session, url=url))
        results.append({
            'url': url,
            'results': await task,
        })
    return results

async def scrape_page_for_urls(soup: BeautifulSoup) -> list[str]:
    """
    Function utilising BeautifulSoup as parameter to scrape a URL of all URLs for each individual movies.
    """
    try:
        if soup is None:
            print(f"[{datetime.datetime.now()}]{Fore.RED} Failed to eat BeautifulSoup...{Style.RESET_ALL}")
            raise("Something went wrong with BeautifulSoup.")
        movie_urls: list = list()
        movies: ResultSet = soup.find_all(name='a', attrs={'class': 'image'})
        for movie in movies:
            # href for url
            movie_urls.append(movie['href'])
        return movie_urls
    except Exception as _exception:
        print(_exception)
        return

async def scrape_cast_details(soup: BeautifulSoup) -> list[str] | None:
    """
    Function to scrape all 'Top Billed Cast' and return it as list.
    """
    if soup:
        cast = soup.find(name='section', attrs={'class': 'panel top_billed scroller'}).find_all(name='li', attrs={'class': 'card'})
        return [_cast.find('p').get_text() for _cast in cast] # get_text() returns str

async def scrape_movie_details(soup: BeautifulSoup) -> list[dict] | None:
    """
    Function to scrape all movie details of each individual URL.
    """
    try:
        data: list[dict] = []

        if soup is None:
            print(f"[{datetime.datetime.now()}]{Fore.RED} Failed to eat BeautifulSoup...{Style.RESET_ALL}")
            raise("Something went wrong with BeautifulSoup.")
        
        # Scrapes whole webpage that URL is on
        movie_content: Tag = soup.find(name='section', attrs={'class': 'inner_content movie_content backdrop poster'})

        # Scrapes title and image URL information
        title_and_image: Tag = movie_content.find(name='div', attrs={'class': 'blurred'})

        # Scrapes overview of the 'selected' movie
        overview: Tag = movie_content.find(name='div', attrs={'class': 'overview'})

        # Create obj/dict with all scraped information and selected attributes
        return ({
            'Title': title_and_image.img.get('alt'),
            'Image URL': title_and_image.img.get('src'),
            'Description': overview.get_text(),
            'Cast': await scrape_cast_details(soup=soup),
        })

    except Exception as _exception:
        print(_exception)
        return

async def main() -> None:
    movie_urls: list[str] = []
    movie_data: list[dict] = []

    # Main page
    async with aiohttp.ClientSession() as session:
        print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping main page...")
        html_page: str = await fetch(session=session)
        soup: BeautifulSoup = BeautifulSoup(
            markup=html_page,
            features='lxml'
        )
        movie_urls = await scrape_page_for_urls(soup)

    # Movie Information
    async with aiohttp.ClientSession() as session:
        print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping movie information...")
        # Returns a list with corresponding URL and HTML as text result
        movies_html_page: list[dict] = await fetch_all(session=session, urls=movie_urls)
        for item in movies_html_page:
            soup: BeautifulSoup = BeautifulSoup(
                markup = item['results'],
                features='lxml'
            )
            movie_data.append(await scrape_movie_details(soup))
        print(movie_data)

if __name__ == '__main__':
    asyncio.run(main())