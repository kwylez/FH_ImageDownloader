import threading
import urllib


class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

        def run(self):
            while True:
                #grabs host from queue
                image_url = self.queue.get()
                download_image_for_url(image_url)

            #grabs urls of hosts and prints first 1024 bytes of page
            #signals to queue job is done
            self.queue.task_done()


def download_image_for_url(url):
    image_file_name = url.split('/')[-1]
    urllib.urlretrieve(url, image_file_name)
