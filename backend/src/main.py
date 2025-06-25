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

    # Main page
    async with aiohttp.ClientSession() as session:
        #print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping main page...")
        html_page: str = await scraper.fetch(session=session)
        soup: BeautifulSoup = BeautifulSoup(
            markup=html_page,
            features='lxml'
        )
        movie_urls = await scraper.scrape_page_for_paths(soup)

    # Movie Information
    async with aiohttp.ClientSession() as session:
        #print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping movie information...")
        # Returns a list with corresponding URL and HTML as text result
        movies_html_page: list[dict] = await scraper.fetch_all(session=session, paths=movie_urls)
        for item in movies_html_page:
            soup: BeautifulSoup = BeautifulSoup(
                markup = item['results'],
                features='lxml'
            )
            movie_data.append(await scraper.scrape_movie_details(soup))
        print(movie_data)
    print(f"[{datetime.datetime.now()}] [{Fore.GREEN}*{Style.RESET_ALL}] Done")

if __name__ == '__main__':
    asyncio.run(main())

