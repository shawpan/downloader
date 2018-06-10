import getopt, sys
import urllib.request
import urllib.parse
import urllib.error
import os
import json
import logging

logging.basicConfig(filename='downloader.log',filemode='a', format='%(levelname)s : %(asctime)s : %(message)s',level=logging.DEBUG)

def generateFileName(url):
    """ Generate unique file name from url

    Parameters:
    url -- url string
    Returns:
    Filename string
    """
    return "_".join(url.strip().replace("://", "/").split('/'))

def getTotalBytes(response):
    """ Get total size of the file in bytes from response

    Parameters:
    response --- response object from server
    Returns:
    Number of bytes
    """
    return float(response.info()['Content-Length'].strip())

def getResponse(url):
    """ Get response object given url

    Parameters:
    url -- url string
    Returns:
    Response object from server
    """
    userAgent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)';
    rangeHeader = 'bytes=0-'
    headers = { 'User-Agent' : userAgent, 'Range' : rangeHeader}
    request = urllib.request.Request(url, headers = headers)

    return urllib.request.urlopen(request)

def download(source, destination, status = None):
    """ Download resource from source to destination

    Parameters:
    source      -- url string
    destination -- path of the directory to save the file
    status      -- (optional) status Queue
    """
    try:
        outputFilePath = destination + '/' + generateFileName(source)
        response = getResponse(source)
        downloadedBytes = 0
        totalBytes = -1
        totalBytes = getTotalBytes(response)
        with open(outputFilePath, "wb") as outFile:
            while downloadedBytes < totalBytes:
                data = response.read(1024)
                outFile.write(data)
                downloadedBytes = outFile.tell()
                if status is not None:
                    percent = float((downloadedBytes / totalBytes))
                    status.put([source, percent])
    except Exception as e:
        logging.exception(e)
        if status is not None:
            status.put([source, -1])
    finally:
        if os.path.exists(outputFilePath) and (totalBytes == -1 or os.path.getsize(outputFilePath) < totalBytes):
            os.remove(outputFilePath)
