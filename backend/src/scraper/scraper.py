import asyncio
import aiohttp
import datetime
from bs4 import BeautifulSoup, ResultSet, Tag
from colorama import init as colorama_init
from colorama import Fore, Style

class Scraper():
    """
    Scraper class object, created upon call and has passed str URL for all the execution.
    """
    def __init__(self, url: str = None):
        """
        Constructor assigning str to a class visible variable.
        """
        self.url: str = url
        self.movie_data: list[str] = []

    # Fetch information of all movies and return list of that data
    async def fetch_information(self):
        """
        Function that fetches information of all movies and return list of that data.
        """

        # Main page
        async with aiohttp.ClientSession() as session:
            print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping main page...")
            html_page: str = await self.fetch(session=session)
            soup: BeautifulSoup = self.scrape(html_page=html_page, features='lxml')
            movie_urls: list[str] = await self.scrape_page_for_urls(soup)

        # Movie Information
        async with aiohttp.ClientSession() as session:
            print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping movie information...")
            # Returns a list with corresponding URL and HTML as text result
            movies_html_page: list[dict] = await self.fetch_all(session=session, urls=movie_urls)
            for item in movies_html_page:
                soup: BeautifulSoup = self.scrape(
                    html_page=item['results'], 
                    features='lxml'
                )
                self.movie_data.append(await self.scrape_movie_details(soup))

        return self.movie_data

    # Function returning BeautifulSoup object each time it's called
    def scrape(self, html_page: str, features: str) -> BeautifulSoup:
        """
        Method for scraping a webpage given that html_page is response of the web in string form.
        """
        return BeautifulSoup(
            markup=html_page,
            features=features
        )

    # Fetch HTML information about a page
    async def fetch(self, session: aiohttp.ClientSession, url: str = 'https://www.themoviedb.org/movie/top-rated/') -> str:
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
        
    # Fetch HTML information about all pages   
    async def fetch_all(self, session: aiohttp.ClientSession, urls: list[str]) -> list[dict]:
        """
        Method for fetching all webpages HTML(s) as raw text when a list is provided.
        """
        web_url = 'https://www.themoviedb.org'
        results: list[dict] = []
        for url in urls:
            url = web_url + url
            task: asyncio.Task = asyncio.create_task(self.fetch(session=session, url=url))
            results.append({
                'url': url,
                'results': await task,
            })
        return results

    async def scrape_page_for_urls(self, soup: BeautifulSoup) -> list[str]:
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

    async def scrape_cast_details(self, soup: BeautifulSoup) -> list[str] | None:
        """
        Function to scrape all 'Top Billed Cast' and return it as list.
        """
        if soup:
            cast = soup.find(name='section', attrs={'class': 'panel top_billed scroller'}).find_all(name='li', attrs={'class': 'card'})
            return [_cast.find('p').get_text() for _cast in cast] # get_text() returns str

    async def scrape_movie_details(self, soup: BeautifulSoup) -> list[dict] | None:
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
                'Cast': await self.scrape_cast_details(soup=soup),
            })

        except Exception as _exception:
            print(_exception)
            return

# Local testing without running FastAPI    
async def main() -> None:
    scraper = Scraper()

    movie_urls: list[str] = []
    movie_data: list[dict] = []

    # Main page
    async with aiohttp.ClientSession() as session:
        print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping main page...")
        html_page: str = await scraper.fetch(session=session)
        soup: BeautifulSoup = BeautifulSoup(
            markup=html_page,
            features='lxml'
        )
        movie_urls = await scraper.scrape_page_for_urls(soup)

    # Movie Information
    async with aiohttp.ClientSession() as session:
        print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping movie information...")
        # Returns a list with corresponding URL and HTML as text result
        movies_html_page: list[dict] = await scraper.fetch_all(session=session, urls=movie_urls)
        for item in movies_html_page:
            soup: BeautifulSoup = BeautifulSoup(
                markup = item['results'],
                features='lxml'
            )
            movie_data.append(await scraper.scrape_movie_details(soup))
        print(movie_data)

if __name__ == '__main__':
    asyncio.run(main())