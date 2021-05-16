import itertools
from itertools import count
import random


import requests
from bs4 import BeautifulSoup

import config
from helpers.cache_tools import file_persistent_cached_generator
from pathant.Converter import converter
from pathant.PathSpec import PathSpec

import time
from selenium import webdriver

profile = webdriver.Firefox(executable_path="/home/finn/PycharmProjects/RestPathAnt/geckodriver")

import logging


logging.basicConfig(level = logging.INFO)

class Scrape(PathSpec):
    def __init__(self, *args, url="any-api.com", **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.MAX = 2

    driver = profile

    def __iter__(self):
        self.scrape_count = count()
        self.i = 0
        self.yet = []
        yield itertools.islice(self(self.url), self.MAX)

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    def __call__(self, url0):
        logging.info(f"0 trying {url0}")
        if not url0. startswith("http"):
            url0 = "https://" + url0

        logging.info(f"33########### tag-links ########33")
        links = list(self.get_landing_page(url0))

        logging.info(f"33########### fill-links ########33: {links}")
        urls2=list(self.get_groups(links))

        logging.info(f"33########### simple path-links ########33: {urls2}")
        urls3 = list(self.get_raw_paths(urls2))

        logging.info(f"33########### concrete links ########33: {urls3}")

        hrefs = list(self.get_single_paths(urls3))

        # First look on the page for downloads, that should be done
        logging.info(f"33########### concrete pages ########33: {hrefs}")
        for href, meta in hrefs:
            time.sleep(random.uniform(0.09, 0.5))
            response = self.driver.get(href)
            time.sleep(1)
            htmlSource = self.driver.page_source
            yield (htmlSource, {'meta':{'url': href}})

    @file_persistent_cached_generator(config.cache + '3.json')
    def get_single_paths(self, urls3):
        hrefs = {}
        for url, meta in urls3:
            try:
                logging.info(f"trying 3 {url}")
                response = self.driver.get(url)
                time.sleep(1)
                htmlSource = self.driver.page_source
                soup = BeautifulSoup(htmlSource, "lxml")

                nav_item = soup.find("div", class_="ng-trigger-shrinkOut")
                links = nav_item.findAll('a')
                _links = [f'https://any-api.com{link.attrs["href"]}' for link in links
                          if link and "href" in link.attrs]
                logging.info(f"found {_links}")

                hrefs.update({u: meta for u in _links})

            except Exception as e:
                logging.error(
                    f"Connection error, maybe timeout, maybe headers, maybe bad connection, continuing elsewhere: {e}")
        return {link: () for link in hrefs}


    @file_persistent_cached_generator(config.cache + '2.json')
    def get_raw_paths(self, urls2):
        urls3 = {}

        for url, meta in urls2:
            try:
                logging.info(f"trying 2 {url}")
                time.sleep(random.uniform(0.1, 1.0))
                response = self.driver.get(url)
                time.sleep(5)
                htmlSource = self.driver.page_source
                soup = BeautifulSoup(htmlSource, "lxml")

                links = soup.findAll('a', {"class": "truncate"})
                links = [f'https://any-api.com{link.attrs["href"]}' for link in links]
                urls3.update({u: meta for u in links})
                logging.info(f"found {links}")
            except Exception as e:
                logging.error(
                    f"Connection error, maybe timeout, maybe headers, maybe bad connection, continuing elsewhere: {e}")
                continue
        return {link: () for link in urls3}

    @file_persistent_cached_generator(config.cache + '1.json')
    def get_groups(self, links):
        urls2 = {}
        for url, meta in links:
            try:
                time.sleep(random.uniform(0.1, 1.0))
                logging.info(f" 1 trying {url}")

                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.text, "lxml")

                _urls2 = soup.findAll('a', {"class": "fill-link"})
                _urls2 = [f'https://any-api.com{link.attrs["href"]}' for link in _urls2]
                random.shuffle(_urls2)
                urls2.update({u: meta for u in _urls2})
                if response.status_code == 404:
                    logging.error(f"404 for {url}")
            except Exception as e:
                logging.error(
                    f"Connection error, maybe timeout, maybe headers, maybe bad connection, continuing elsewhere: {e}")

        return {link: () for link in urls2}

    @file_persistent_cached_generator(config.cache + '0.json')
    def get_landing_page(self, url0):
        try:
            response = requests.get(url0, headers=self.headers)
            soup = BeautifulSoup(response.text, "lxml")

            links = soup.findAll('a', {"class": "tag-link"})
            links = [f'{url0}/?tag={link.text}' for link in links]
            random.shuffle(links)
            if response.status_code == 404:
                logging.error(f"404 for {url0}")
        except Exception as e:
            logging.error(
                f"Connection error, maybe timeout, maybe headers, maybe bad connection, continuing elsewhere: {e}")
        return list({link: () for link in links}.items())





