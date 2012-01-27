#!/usr/bin/env python
from lib.utils.decorators import async


# Fetch Paths to Images
@async
def fetch_image_paths():
    return 'Hello world'


# Fetch Images for Paths


if __name__ == "__main__":
    fetch_image_paths()
