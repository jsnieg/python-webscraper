import asyncio
import requests
import aiohttp
import datetime
from bs4 import BeautifulSoup, ResultSet, Tag
from colorama import init as colorama_init
from colorama import Fore, Style

web_url = 'https://www.themoviedb.org'

async def fetch(session: aiohttp.ClientSession, url: str = 'https://www.themoviedb.org/movie/') -> str:
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

async def scrape_movie_details(soup: BeautifulSoup) -> list[dict] | None:
    """
    Function to scrape all movie details of each individual URL.
    """
    try:
        data: list[dict] = []
        cast_list: list[str] = []

        if soup is None:
            print(f"[{datetime.datetime.now()}]{Fore.RED} Failed to eat BeautifulSoup...{Style.RESET_ALL}")
            raise("Something went wrong with BeautifulSoup.")
        
        # Scrapes whole webpage that URL is on
        movie_content: Tag = soup.find(name='section', attrs={'class': 'inner_content movie_content backdrop poster'})

        # Scrapes title and image URL information
        title_and_image: Tag = movie_content.find(name='div', attrs={'class': 'blurred'})

        # Scrapes overview of the 'selected' movie
        overview: Tag = movie_content.find(name='div', attrs={'class': 'overview'})

        # Attempt to scrape [Top] cast of the movie
        cast: Tag = movie_content.find(name='section', attrs={'class': 'panel top_billed scroller'})
        cast = cast.find(name='ol', attrs={'class': 'people scroller'}).find_all('li', attrs={'class': 'card'})
        for _cast in cast:
            cast_list.append(str(_cast.text).strip('\n'))
        print(cast_list[::2])

        # Create obj/dict with all scraped information and selected attributes
        data.append({
            'Title': title_and_image.img.get('alt'),
            'Image URL': title_and_image.img.get('src'),
            'Description': overview.get_text(),
            'Cast': None,
        })
        # print(data)
        return data
    except Exception as _exception:
        print(_exception)
        return

async def main() -> None:
    async with aiohttp.ClientSession() as session:
        html_page: str = await fetch(session=session)
        soup: BeautifulSoup = BeautifulSoup(
            markup=html_page,
            features='lxml'
        )
        movie_urls = await scrape_page_for_urls(soup)

    async with aiohttp.ClientSession() as session:
        # Returns a list with corresponding URL and HTML as text result
        movies_html_page: list[dict] = await fetch_all(session=session, urls=movie_urls)
        for item in movies_html_page:
            soup: BeautifulSoup = BeautifulSoup(
                markup = item['results'],
                features='lxml'
            )
            await scrape_movie_details(soup)

if __name__ == '__main__':
    asyncio.run(main())