# Scrape Package
from scraper.scraper import Scraper

# FastAPI
from typing import Annotated
from fastapi import Body, FastAPI, Request, HTTPException
from pydantic import BaseModel, Field

web_url = 'https://www.themoviedb.org'

app = FastAPI()

# When POST is called, scraper is assigned with Scraper() class.
scraper = Scraper()

# TODO:
# Scrape more than 1 page
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
async def status() -> dict:
    """
    **[GET]**

    Call this GET method to see status of the API, whether the call was authorised or not.
    """
    # TODO; add auth logic?
    return {'Response': str(True)}

@app.get("/get_url")
async def get_url() -> dict:
    """
    **[GET]**

    A function that returns the set url when POST request was called.
    """
    try:
        if scraper.url == None:
            raise HTTPException(status_code=404, detail='No URL was set. Use [/set_options] endpoint to set one.')
        return {'Response': scraper.url}
    except AttributeError as _exception:
        return {'Response': _exception}

movie_data: list[str] = []
@app.get("/scrape_pages")
async def scrape_pages() -> dict:
    """
    **[GET]**

    Function to fetch all information about the movies by scraping each URL individually.
    """
    try:
        movie_data: list[str] = await scraper.fetch_information()
        return {'Response': movie_data}
    except Exception as _exception:
        print(_exception)
        return {'Response': 'Error'}

@app.post("/set_options")
async def set_options(
    url: str, 
    pages: int = 1, 
    scrape_url: ScrapeURL = ScrapeURL
) -> dict:
    """
    **[POST]**

    A function that sets current str for usage.

    Only acceptable URL is TMDB (https://www.themoviedb.org).

    Set amount pages you wish to scrape, default is 1. Recommended value is between 3/5.

    **Parameters**:

    url (string) variable that sets a URL to scrape\n
    pages (int) variable that sets how many pages to scrape by default is 1 
    """
    # https://stackoverflow.com/questions/71260288/how-to-share-variables-between-http-requests-in-fastapi
    scraper.url = url
    scraper.pages = pages
    return {
        'Response': {
            'URL': scraper.url,
            'Pages': scraper.pages
        }
    }