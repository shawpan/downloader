import getopt, sys
import os
import json
import collections
from multiprocessing import Process as Task, Queue
import logging

logging.basicConfig(filename='downloader.log',filemode='a', format='%(levelname)s : %(asctime)s : %(message)s',level=logging.DEBUG)

def printProgress(progress):
    """ Print down load progress on screen

    Parameters:
    progress -- progress object containing download percent of each item
    """
    sys.stdout.write('\033[2J\033[H') # clear screen
    for url, percent in progress.items():
        if percent == -1: # -1 means download failed
            sys.stdout.write("%s [ Failed to download ]\n" % (url))
            continue
        bar = ('=' * int(percent * 100)).ljust(100)
        percent = float(percent * 100.0)
        sys.stdout.write("%s [%s] %s%%\n" % (url, bar, round(percent, 2)))
    sys.stdout.flush()

def startProgressDisplay(workers, status, progress):
    """ Initiate the prining process of download status

    Parameters:
    workers  -- array of workers
    status   -- status Queue of workers
    progress -- progress object containing download percent of each item
    """
    while any(worker.is_alive() for worker in workers):
        time.sleep(0.1)
        while not status.empty():
            url, percent = status.get()
            progress[url] = percent
            printProgress(progress)

def startDownLoadTask(singleDownLoader, url, destination, status, workers, progress):
    """ Start a child process to download from given url

    Parameters:
    singleDownLoader -- download method to download given url
    url              -- url string
    destination      -- path of the directory to save the file
    status           -- status Queue of workers
    workers          -- array of workers
    progress         -- progress object containing download percent of each item
    """
    child = Task(target=singleDownLoader, args=(url, destination, status))
    child.start()
    workers.append(child)
    progress[url] = 0.0

def download(sources, singleDownLoaderMethod, destination):
    """ Download resources from given sources to destination

    Parameters:
    sources                -- iterable object of download sources/urls
    singleDownLoaderMethod -- download method to download given url
    destination            -- path of the directory to save the file
    """
    status = Queue()
    progress = collections.OrderedDict()
    workers = []
    try:
        for url in sources:
            startDownLoadTask(singleDownLoaderMethod, url, destination, status, workers, progress)
        startProgressDisplay(workers, status, progress)
    except Exception as e:
        logging.exception(e)
