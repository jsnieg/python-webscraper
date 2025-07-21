# TMDB Webscraper

## Introduction

This repository or a rather demonstration of `BeautifulSoup3` in scraping movie information from [TMDB](https://www.themoviedb.org/) and displaying it to a user through `FastAPI` in form of automatically generated documentation using `Swagger`.

Both, .json and console output are available to the user without the need for a database, although, that could potentially add to the completion of the repo.

Shifting focus from creating a web scraper of job postings to something more **free**, **legal** and **easier** from [TMDB](https://www.themoviedb.org/) which does not infringe on user's private data and displays it onto a React front-end with Python back-end by pressing a button 'Scrape'. As I have found a major roadblock and most internet devs struggled in creating a scraper of latter idea. I want to learn and not rip my hair out.

Feel free to fork, clone and tinker with it. This is part of my ever "expanding" portoflio to showcase my understanding of development on a much smaller scale like personal development to enhance my ability to solve problems and atmost learn, learn and learn.

A To Do list:

- Working WebScraper where it scrapes `n` pages instead of just one -> **[?]**
- Working FastAPI backend -> **[x]**
- Working Authentication method -> **[]**
- Working a React front-end (optional) -> **[]**
- Working Docker deployment -> **[]**

## Requirements

- Python 3.12+
- React + Vite
- Colorama (console text color)
- BeautifulSoup
- Asyncio HTTP
- FastAPI

## Running Locally

### Windows

1. Clone the repository

    - `git clone https://github.com/jsnieg/python-webscraper.git <optional directory>`

2. Install dependecies

    - Move into the directory `cd python-webscraper`
    - `pip install -r 'requirements.txt'`

3. Running the backend

    - `python backend/src/run.py` or `cd backend/src/api` then `fastapi run api.py`.

### Linux (Ubuntu)

`Work in Progress`.

1. Clone the repository

    - `git clone https://github.com/jsnieg/python-webscraper.git <optional directory>`

2. Move into the directory `cd <your directory>`

3. Create a Python Virtual Environment (to not install packages system-wide)

    - python -m venv /path/to/new/virtual/env

4. Run `/path/to/venv/<your venv>/bin/pip install -r requirements.txt`

5. Test running `/path/to/env/<your env>/bin/python backend/src/main.py` *should run the script.*

6. Test running `/path/to/env/<your env>/bin/fastapi run backend/src/api/api.py` *it should run fastapi with docs, alternatively replace run with dev for hot-reload*.

## Authors

Janusz Snieg

## Copyright

TBA

## Findings

- This is a very first personal project where I sat down and actually coded something up by just using documentation, form of AI only for troubleshooting, relying on Stacks and articles found.

- When moving development onto Linux, I came across issues of the OS refusal of installing packages on system-wide scale. Hence, I needed to move into virtual environemnts. As a challenge, I did not want to use `anaconda` but rather built-in `python` v-env and being able to successfully to run the script same way it did on Windows.