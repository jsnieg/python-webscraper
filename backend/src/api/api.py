# Scrape Package
from scraper.scraper import Scraper

# FastAPI
from typing import Annotated
from fastapi import Body, FastAPI, Request
from pydantic import BaseModel, Field

web_url = 'https://www.themoviedb.org'

app = FastAPI()

# When POST is called, scraper is assigned with Scraper() class.
scraper = Scraper()

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
        return {'Response': app.state.url, 'Class': scraper.url}
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
        movie_data: list[str] = await scraper.fetch_information()
        return {'Response': movie_data}
    except Exception as _exception:
        print(_exception)
        return {'Response': 'Error'}

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
    scraper.url = url
    return {'Response': app.state.url}