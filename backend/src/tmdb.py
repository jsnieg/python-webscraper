import asyncio
import requests
import aiohttp
import datetime
from bs4 import BeautifulSoup, ResultSet
from colorama import init as colorama_init
from colorama import Fore, Style

web_url = 'https://www.themoviedb.org'

async def scrape_page(urls):
    soup: BeautifulSoup = BeautifulSoup(
        markup = url
    )

async def fetch(session: aiohttp.ClientSession, url: str = 'https://www.themoviedb.org/movie/') -> str:
    """"""
    async with session.get(url) as response:
        if response.status == 200:
            print(f"[{datetime.datetime.now()}]{Fore.GREEN} Response [{response.status}]{Style.RESET_ALL}")
            return await response.text()
        if response.status == 429:
            print(f"[{datetime.datetime.now()}]{Fore.RED} Response [{response.status}]{Style.RESET_ALL}")
        else:
            response.raise_for_status()
    
async def fetch_all(session: aiohttp.ClientSession, urls: list[str]) -> list[dict]:
    """"""
    results: list[dict] = []
    # tasks: list = []
    for url in urls:
        url = web_url + url
        print(url)
        task: asyncio.Task = asyncio.create_task(fetch(session=session, url=url))
        results.append({
            'url': url,
            'results': await task,
        })
        # tasks.append(task)
    # results = await asyncio.gather(*tasks) # * in this context means unpacking list
    return results

async def main():
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
        print(movie_urls)
        
    async with aiohttp.ClientSession() as session:
        # Returns 
        movies_html_page: list[dict] = await fetch_all(session=session, urls=movie_urls)
        first_movie = movies_html_page[0]['results']
        soup: BeautifulSoup = BeautifulSoup(
            markup = first_movie,
            features='lxml'
        )
        # print(soup)
        media_results = soup.find(name='section', attrs={'id': 'original_header'})
        # media_results.find('div', attrs={'class': 'blurred'})
        print(media_results.find('div', attrs={'class': 'blurred'}))
        l = media_results.find('div', attrs={'class': 'blurred'})
        for _l in l:
            print(l.img.get('alt'))

if __name__ == '__main__':
    asyncio.run(main())