import asyncio
import requests
import aiohttp
import datetime
from bs4 import BeautifulSoup, ResultSet
from colorama import init as colorama_init
from colorama import Fore, Style

web_url = 'https://www.themoviedb.org'

async def scrape_page(urls):
    pass

async def scrape_movie_details():
    pass

async def fetch(session: aiohttp.ClientSession, url: str = 'https://www.themoviedb.org/movie/') -> str:
    """
    Method for fetching webpage HTML as raw text.
    """
    print(f"[{datetime.datetime.now()}] Fetching HTML of URL [{Fore.BLUE}{url}{Style.RESET_ALL}]")
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

async def main() -> None:
    movie_urls: list = list()
    async with aiohttp.ClientSession() as session:
        html_page: str = await fetch(session=session)
        soup: BeautifulSoup = BeautifulSoup(
            markup=html_page,
            features='lxml'
        )
        media_results = soup.find(name='section', attrs={'id': 'media_results'})
        movies: ResultSet = soup.find_all(name='a', attrs={'class': 'image'})
        for movie in movies:
            # href for url
            movie_urls.append(movie['href'])
        
    async with aiohttp.ClientSession() as session:
        # Returns a list with corresponding URL and HTML as text result
        movies_html_page: list[dict] = await fetch_all(session=session, urls=movie_urls)
        for item in movies_html_page:
            soup: BeautifulSoup = BeautifulSoup(
                markup = item['results'],
                features='lxml'
            )
            media_results = soup.find(name='section', attrs={'id': 'original_header'})
            l = media_results.find('div', attrs={'class': 'blurred'})
            for _l in l:
                print(l.img.get('alt'))

if __name__ == '__main__':
    asyncio.run(main())