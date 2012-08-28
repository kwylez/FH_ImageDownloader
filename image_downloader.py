#!/usr/bin/env python

import httplib2
import urllib

from BeautifulSoup import BeautifulSoup, SoupStrainer
# from lib.utils.decorators import async

FRESH_HOMES_ROOT_URL = 'http://freshome.com/'
DEBUG = False


# Fetch Paths to Images
def fetch_image_paths(url):

    http = httplib2.Http()
    status, response = http.request(url)
    soup = BeautifulSoup(response)
    all_image_links = []

    try:
        entry_div = soup.findAll('div', attrs={'class': 'entry_text'})
        for div in entry_div:
            for paragraph in div.findAll("p"):
                all_image_links = paragraph.findAll({'img': True})

    except TypeError:
        print "It failed getting from %s" % url

    return all_image_links


def download_image_for_url(url):
    if DEBUG:
        print "image to download %s\n" % url
    image_file_name = url.split('/')[-1]
    urllib.urlretrieve(url, image_file_name)


def find_latest_posts():
    http = httplib2.Http()
    status, response = http.request(FRESH_HOMES_ROOT_URL)
    soup = BeautifulSoup(response, parseOnlyThese=SoupStrainer('h1'))

    # Find all the 'a' tags skipping the first which is the homepage
    all_links = soup.findAll({'a': True})[1:]

    return all_links


if __name__ == "__main__":

    print "Fetch all images to download...\n"

    for link in find_latest_posts():
        try:
            print link['href']
            print "Fetching image for %s\n" % link['href']
            for image_link in fetch_image_paths(link['href']):
                print "Source link: %s" % image_link['src']
                download_image_for_url(image_link['src'])
        except KeyError:
            pass
