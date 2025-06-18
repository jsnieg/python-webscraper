import asyncio
import requests
import aiohttp
from bs4 import BeautifulSoup, ResultSet

web_url = 'https://www.themoviedb.org'

async def fetch(session: aiohttp.ClientSession, url: str = 'https://www.themoviedb.org/movie/') -> str:
    async with session.get(url) as response:
        if response.status != 200:
            response.raise_for_status()
        # print(await response.text())
        return await response.text()
    
async def fetch_all(session: aiohttp.ClientSession, urls: list[str]):
    tasks: list = []
    for url in urls:
        task = asyncio.create_task(fetch(session=session, url=web_url+url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
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
        # print(await fetch_all(session, movie_urls))
        # print([movie for movie in movie_urls][0])
        print(await fetch(session=session, url=web_url+[movie for movie in movie_urls][0]))

if __name__ == '__main__':
    asyncio.run(main())