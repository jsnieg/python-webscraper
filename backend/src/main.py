import aiohttp
import asyncio
import datetime

from scraper.scraper import Scraper
from bs4 import BeautifulSoup
from colorama import init as colorama_init
from colorama import Fore, Style

# Local testing without running FastAPI    
async def main() -> None:
    scraper = Scraper()

    movie_urls: list[str] = []
    movie_data: list[dict] = []

    # url: str = 'https://www.themoviedb.org/'
    url: str = 'https://www.themoviedb.org/movie/now-playing'
    #'https://www.themoviedb.org/movie/now-playing'

    scraper.url = url

    # Main page
    async with aiohttp.ClientSession() as session:
        html_page: str = await scraper.fetch(session=session, url=url)
        soup: BeautifulSoup = BeautifulSoup(
            markup=html_page,
            features='lxml'
        )
        movie_urls = await scraper.scrape_page_for_paths(soup)
        print(movie_urls)

    # Movie Information
    async with aiohttp.ClientSession() as session:
        # Returns a list with corresponding URL and HTML as text result
        movies_html_page: list[dict] = await scraper.fetch_all(session=session, paths=movie_urls)
        for item in movies_html_page:
            soup: BeautifulSoup = BeautifulSoup(
                markup = item['results'],
                features='lxml'
            )
            movie_data.append(await scraper.scrape_movie_details(soup))
        print(movie_data)

    import json
    with open('examples/movie_data.json', 'w', encoding='utf-8') as f:
        json.dump(movie_data, f, ensure_ascii=False, indent=4)

    print(f'Movie toll: {scraper.movie_count}')
    print(f'Steps taken: {scraper.steps}')
    print(f"[{datetime.datetime.now()}] [{Fore.GREEN}*{Style.RESET_ALL}] Done")

if __name__ == '__main__':
    asyncio.run(main())