import unittest
import urllib.request
import urllib.error
import collections
from unittest.mock import patch, MagicMock
from multiprocessing import Process as Task, Queue

import single_downloader
import multiple_downloader

class TestMultipleDownloader(unittest.TestCase):
    def setUp(self):
        self.sources = ['abc://def.gh']
        self.destination = 'path/to/dest'
        self.singleDownLoaderMethod = MagicMock()
        self.singleDownLoaderMethod.return_value = None

    @patch('multiple_downloader.startDownLoadTask')
    @patch('multiple_downloader.startProgressDisplay')
    def testDownload(self, mockStartProgressDisplay, mockStartDownLoadTask):
        mockStartDownLoadTask.return_value = None
        mockStartProgressDisplay.return_value = None
        multiple_downloader.download(self.sources,
                                    self.singleDownLoaderMethod,
                                    self.destination)
        self.assertEqual(mockStartDownLoadTask.call_count, len(self.sources))
        self.assertEqual(mockStartProgressDisplay.call_count, 1)

if __name__ == '__main__':
    unittest.main()
