#!/usr/bin/env python

import httplib2
import urllib
import errno
import os
from threading import Thread

from BeautifulSoup import BeautifulSoup, SoupStrainer

# from lib.utils.imagethreading import ThreadUrl
# from lib.utils.decorators import async

FRESH_HOMES_ROOT_URL = 'http://freshome.com/'
DEBUG = False

def make_require_dir(path):
    try:
        os.makedirs(path)
    except OSError, exc:
        if exc.errno != errno.EEXIST:
            raise


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

    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fh-images")
    make_require_dir(directory)

    # url encode for special characters or it will fail
    url = unicode(url)
    url = url.encode('utf-8')

    # grab the image name from url
    image_file_name = url.split('/')[-1]
    filename = os.path.join(directory, image_file_name)

    if not os.path.exists(filename):
        urllib.urlretrieve(url, filename)


def find_latest_posts():

    http = httplib2.Http()
    status, response = http.request(FRESH_HOMES_ROOT_URL)

    if DEBUG:
        print "Status %s" % status

    if (status.status == 200):
        soup = BeautifulSoup(response, parseOnlyThese=SoupStrainer('h1'))

        # Find all the 'a' tags skipping the first which is the homepage
        all_links = soup.findAll({'a': True})[1:]

    return all_links


if __name__ == "__main__":

    print "Fetch all images to download...\n"

    for link in find_latest_posts():
        try:
            if DEBUG:
                print link['href']
            print "Fetching image for %s\n" % link['href']

            for image_link in fetch_image_paths(link['href']):
                if DEBUG:
                    print "Source link: %s" % image_link['src']

                t = Thread(target=download_image_for_url, args=(image_link['src'],))
                t.start()
        except KeyError:
            pass
