# Scrape Package
from scraper.scraper import *

# FastAPI
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
    [GET]
    Call this GET method to see if API is infact working as intended.
    """
    return {'Fast':'API'}

@app.get("/get_url")
async def get_url() -> dict:
    """
    [GET]
    A function that returns the set url when POST request was called.
    """
    try:
        return {'Response': app.state.url}
    except AttributeError as _exception:
        return {'Response': _exception}

movie_data: list[str] = []
@app.get("/scrape_page")
async def scrape_page() -> dict:
    """
    [GET]
    Function to fetch all urls on the site.
    """
    try:
        url: str = str(app.state.url)

        # Main page
        async with aiohttp.ClientSession() as session:
            print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping main page...")
            # html_page: str = await fetch(session=session, url=url)
            html_page: str = await fetch(session=session)
            soup: BeautifulSoup = BeautifulSoup(
                markup=html_page,
                features='lxml'
            )
            app.state.movie_urls = await scrape_page_for_urls(soup)
            # return {'Response': app.state.movie_urls}
        
        # Movie Information
        async with aiohttp.ClientSession() as session:
            print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping movie information...")
            # Returns a list with corresponding URL and HTML as text result
            movies_html_page: list[dict] = await fetch_all(session=session, urls=app.state.movie_urls)
            for item in movies_html_page:
                soup: BeautifulSoup = BeautifulSoup(
                    markup = item['results'],
                    features='lxml'
                )
                movie_data.append(await scrape_movie_details(soup))
        return {'Response': movie_data}
    except Exception as _exception:
        return {'Response': _exception}

@app.post("/set_url")
# async def set_url(url: str | None, scrape_url: Annotated[ScrapeURL, Body(embed=True)]) -> str:
async def set_url(url: str, scrape_url: ScrapeURL) -> dict:
    """
    [POST]
    A function that sets current str for usage.

    Only acceptable URL is TMDB (https://www.themoviedb.org).
    """
    # https://stackoverflow.com/questions/71260288/how-to-share-variables-between-http-requests-in-fastapi
    app.state.url = url
    return {'Response': app.state.url}