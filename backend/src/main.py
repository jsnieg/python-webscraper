# Requirements
# - python 3.12
# - playwright
#   - run: playwright install (this installs all compatible browsers)
# - django

# Libraries
import asyncio
import django
from playwright.async_api import async_playwright

unavailable_version: str = "VERSION UNAVAILABLE"

async def main() -> None:
    print("It's empty here, but hopefully we'll get some basic web scraping going.")
    async with async_playwright() as pw:
        browsers: list = [pw.firefox]
        for browser_type in browsers:
            browser = await browser_type.launch()
            page = await browser.new_page()
            await page.goto('http://playwright.dev')
            await page.screenshot(path=f'misc/example-{browser_type.name}.png')
            await browser.close()

if __name__ == "__main__":
    print("Version prints of all libraries...")
    print(f"Django - {django.get_version()}\nPlaywright - {unavailable_version}")
    asyncio.run(main())