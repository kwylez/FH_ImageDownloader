#!/usr/bin/env python
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
from lib.utils.decorators import async


FRESH_HOMES_ROOT_URL = 'http://freshome.com/'


# Fetch Paths to Images
@async
def fetch_image_paths():
    return 'Hello world'


def find_latest_posts():
    http = httplib2.Http()
    status, response = http.request(FRESH_HOMES_ROOT_URL)
    soup = BeautifulSoup(response, parseOnlyThese=SoupStrainer('h2'))
    return soup.findAll({'a': True})


if __name__ == "__main__":

    for link in find_latest_posts():
        try:
            print link['href']
        except KeyError:
            pass
