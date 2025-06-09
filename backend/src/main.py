# Requirements
# - python 3.12
# - playwright
#   - run: playwright install (this installs all compatible browsers)
# - django

# Libraries
import asyncio
import django
import urllib.parse
from playwright.async_api import async_playwright

unavailable_version: str = "VERSION UNAVAILABLE"


async def main() -> None:
    print('Setting default values for searching...')
    text: str = 'Software Developer Jobs'
    term: str = urllib.parse.quote_plus(text)
    URL: str = f'http://www.google.com/search?q={term}'

    print("It's empty here, but hopefully we'll get some basic web scraping going.")
    async with async_playwright() as pw:
        browsers: list = [pw.firefox]
        try:
            for browser_type in browsers:
                browser = await browser_type.launch()
                page = await browser.new_page()
                print(f'Going to the URL... {URL}\nFilling a text field area with input... {text}')
                await page.goto(URL)
                print(f"Please, don't arrest me... I have no ill aim.")
                frame = page.frame_locator("iframe[title='reCAPTCHA']")
                label = frame.locator("#recaptcha-anchor-label")
                print(label)
                await page.get_by_label(label).set_checked(True)
                print(f'Taking a screenshot for testing...')
                await page.screenshot(path=f'misc/example-{browser_type.name}.png') 
                print(f'Closing browser...')
                await browser.close()
        except Exception as _exception:
            print(_exception)

if __name__ == "__main__":
    print("Version prints of all libraries...")
    print(f"Django - {django.get_version()}\nPlaywright - {unavailable_version}")
    asyncio.run(main())