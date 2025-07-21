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

- Python 3.13+
- React + Vite
- Colorama (console text color)
- BeautifulSoup
- AIO HTTP
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

## Authors

Janusz Snieg

## Copyright

TBA