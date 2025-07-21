import asyncio
import aiohttp
import datetime
from bs4 import BeautifulSoup, ResultSet, Tag
from colorama import init as colorama_init
from colorama import Fore, Style
from urllib.parse import urlparse, ParseResult

class Scraper():
    """
    Scraper class object, created upon call and has passed str URL for all the execution.
    """
    def __init__(
            self, 
            url: str = None,
            pages: int = None
        ):
        """
        Constructor assigning str to a class visible variable.
        """
        self.url: str = url
        self.pages = pages
        self.movie_data: list[str] = []
        self.movie_count: int = 0
        self.steps: int = 0

    async def fetch_information(self):
        """
        Function that fetches information of all movies and return list of that data.
        """

        # Main page
        async with aiohttp.ClientSession() as session:
            print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping main page...")
            html_page: str = await self.fetch(session=session)
            soup: BeautifulSoup = self.scrape(html_page=html_page, features='lxml')
            movie_paths: list[str] = await self.scrape_page_for_paths(soup)

        # Movie Information
        async with aiohttp.ClientSession() as session:
            print(f"[{datetime.datetime.now()}] [{Fore.BLUE}*{Style.RESET_ALL}] Scraping movie information...")
            # Returns a list with corresponding URL and HTML as text result
            movies_html_page: list[dict] = await self.fetch_all(session=session, paths=movie_paths)
            for item in movies_html_page:
                soup: BeautifulSoup = self.scrape(
                    html_page=item['results'], 
                    features='lxml'
                )
                self.movie_data.append(await self.scrape_movie_details(soup))

        print(f"[{datetime.datetime.now()}] [{Fore.GREEN}*{Style.RESET_ALL}] Done")
        return self.movie_data

    def scrape(
            self, 
            html_page: str, 
            features: str
        ) -> BeautifulSoup:
        """
        Method for scraping a webpage given that html_page is response of the web in string form.
        """
        return BeautifulSoup(
            markup=html_page,
            features=features
        )

    # TODO: when fetch is called no url is set therefore default is used
    async def fetch(
            self, 
            session: aiohttp.ClientSession, 
            url: str
        ) -> str:
        """
        Method for fetching webpage HTML as raw text.
        """
        # print(f"[{datetime.datetime.now()}] Fetching HTML of URL: [{Fore.BLUE}{url}{Style.RESET_ALL}] w/", end=" ")
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    #print(f"{Fore.GREEN}Response [{response.status}]{Style.RESET_ALL}")
                    return await response.text()
                if response.status == 429:
                    print(f"{Fore.RED}Response [{response.status}]{Style.RESET_ALL}")
                else:
                    response.raise_for_status()
        except Exception as _exception:
            print(_exception)
           
    async def fetch_all(
            self, 
            session: aiohttp.ClientSession, 
            paths: list[str]
        ) -> list[dict]:
        """
        Method for fetching all webpages HTML(s) as raw text when a list is provided.
        """
        #https://www.themoviedb.org/movie?page=2
        results: list[dict] = []
        parsed_url: ParseResult = urlparse(self.url)
        parsed_url: str = f'{parsed_url.scheme}://{parsed_url.netloc}'
        # for i in range(0, 3):
        #     print(f'{self.url}?page={i}')
        #     for path in paths:
        #         url = f'{parsed_url}{path}?page={i}'
        #         print(url)
        #         task: asyncio.Task = asyncio.create_task(self.fetch(session=session, url=url))
        #         results.append({
        #             'url': url,
        #             'results': await task,
        #         })
        # return results

        for path in paths:
            url = parsed_url + path
            print(url)
            task: asyncio.Task = asyncio.create_task(self.fetch(session=session, url=url))
            results.append({
                'url': url,
                'results': await task,
            })
            self.steps += 1
        return results

    async def scrape_page_for_paths(
            self, 
            soup: BeautifulSoup
        ) -> list[str]:
        """
        Function utilising BeautifulSoup as parameter to scrape a URL of all paths for each individual movies.
        """
        try:
            movie_paths: list = list()
            movies: ResultSet = soup.find_all(name='a', attrs={'class': 'image'})
            for movie in movies:
                # href for url
                movie_paths.append(movie['href'])
            # Keep record of movies count on a page 
            self.movie_count = len(movie_paths)
            return movie_paths
        except Exception as _exception:
            print(_exception)
            return

    async def scrape_cast_details(
            self, 
            soup: BeautifulSoup
        ) -> list[str] | None:
        """
        Function to scrape all 'Top Billed Cast' and return it as list.
        """
        if soup:
            cast = soup.find(name='section', attrs={'class': 'panel top_billed scroller'}).find_all(name='li', attrs={'class': 'card'})
            return [_cast.find('p').get_text() for _cast in cast] # get_text() returns str

    async def scrape_movie_details(
            self, 
            soup: BeautifulSoup
        ) -> list[dict] | None:
        """
        Function to scrape all movie details of each individual URL.
        """
        try:
            data: list[dict] = []
            
            # Scrapes whole webpage that URL is on
            movie_content: Tag = soup.find(name='section', attrs={'class': 'inner_content movie_content backdrop poster'})
            # print(movie_content)

            # Scrapes title and image URL information
            title_and_image: Tag = movie_content.find(name='div', attrs={'class': 'blurred'})
            # print(title_and_image)

            # Scrapes overview of the 'selected' movie
            overview: Tag = movie_content.find(name='div', attrs={'class': 'overview'})
            # print(overview)

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