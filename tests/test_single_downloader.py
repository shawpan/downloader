import unittest
import urllib.request
import urllib.error
from unittest.mock import patch, MagicMock

import single_downloader

class TestSingleDownloader(unittest.TestCase):
    def setUp(self):
        userAgent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)';
        rangeHeader = 'bytes=0-'
        self.requestHeaders = { 'User-Agent' : userAgent, 'Range' : rangeHeader}
        self.url = 'http://ab.com/cd.ef'
        self.filename = 'http_ab.com_cd.ef'
        self.destination = '/user/dest'

        c = MagicMock()
        c.info.return_value = {'Content-Length': '128'};
        c.return_value = "abcd"
        c.__enter__.return_value = c
        self.context = c

    def testGenerateFileName(self):
        fileName = single_downloader.generateFileName(self.url)
        self.assertEqual(fileName, self.filename)

    @patch('urllib.request.urlopen')
    def testGetTotalBytes(self, mockUrlOpen):
        mockUrlOpen.return_value = self.context
        with urllib.request.urlopen(self.url) as response:
            totalBytes = single_downloader.getTotalBytes(response)
            self.assertEqual(totalBytes, 128.0)

    @patch('urllib.request.Request')
    @patch('urllib.request.urlopen')
    def testGetResponse(self, mockUrlOpen, mockUrlRequest):
        mockUrlRequest.return_value = self.context
        single_downloader.getResponse(self.url)
        mockUrlRequest.assert_called_once_with(self.url, headers=self.requestHeaders)
        self.assertTrue(mockUrlOpen.called)

    @patch('single_downloader.generateFileName')
    @patch('single_downloader.getResponse')
    @patch('single_downloader.getTotalBytes')
    def testDownload(self, mockGetTotalBytes, mockGetResponse, mockGenerateFileName):
        mockGenerateFileName.return_value = self.filename
        mockGetTotalBytes.return_value = 128.0

        response = MagicMock()
        response.read.return_value = "abcd"
        response.__enter__.return_value = response
        mockGetResponse.return_value = response

        mockOpen = unittest.mock.mock_open()
        with patch('single_downloader.open', mockOpen, create=True):
            single_downloader.download(self.url, self.destination)
            mockOpen.assert_called_once_with(self.destination + '/' + self.filename, "wb")
            handle = mockOpen()
            handle.write.assert_called_with('abcd')
            self.assertTrue(handle.tell)

        mockGenerateFileName.assert_called_once_with(self.url)
        mockGetResponse.assert_called_once_with(self.url)
        mockGetTotalBytes.assert_called_once_with(response)
        mockGetResponse().read.assert_called_with(1024)

    @patch('single_downloader.generateFileName')
    @patch('single_downloader.getResponse')
    @patch('single_downloader.getTotalBytes')
    @patch('os.path.exists')
    def testDownloadFailure(self, mockOsPathExits, mockGetTotalBytes, mockGetResponse, mockGenerateFileName):
        mockGenerateFileName.return_value = self.filename
        mockGetTotalBytes.return_value = 128.0
        mockOsPathExits.return_value = False
        mockGetResponse.side_effect = urllib.error.URLError('Not found')

        mockOpen = unittest.mock.mock_open()
        with patch('single_downloader.open', mockOpen, create=True):
            single_downloader.download(self.url, self.destination)
            self.assertRaises(Exception, mockGetResponse, self.url)
            mockOsPathExits.assert_called_once_with(self.destination + '/' + self.filename)

    @patch('single_downloader.generateFileName')
    @patch('single_downloader.getResponse')
    @patch('single_downloader.getTotalBytes')
    @patch('os.path.exists')
    @patch('os.path.getsize')
    @patch('os.remove')
    def testRemoveFileOnDownloadFailure(self, mockOsRemove, mockOsPathGetsize, mockOsPathExits, mockGetTotalBytes, mockGetResponse, mockGenerateFileName):
        mockGenerateFileName.return_value = self.filename
        mockGetTotalBytes.return_value = 128.0
        mockOsPathGetsize.return_value = 0.0
        response = MagicMock()
        response.read.return_value = "abcd"
        response.__enter__.return_value = response
        mockGetResponse.return_value = response
        mockOsPathExits.return_value = True

        mockOpen = unittest.mock.mock_open()
        with patch('single_downloader.open', mockOpen, create=True):
            mockOpen.side_effect = Exception('Permission error')
            single_downloader.download(self.url, self.destination)
            mockOsRemove.assert_called_once_with(self.destination + '/' + self.filename)

if __name__ == '__main__':
    unittest.main()
