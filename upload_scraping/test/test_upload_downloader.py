try:
    import os
    import unittest
    from dotenv import load_dotenv
    from upload_scraping.src.upload_downloader import UploadDownloader
    from upload_scraping.src.exceptions import LinkIsDown
    from upload_scraping.src.utils.utils import Utils
except ImportError:
    raise ImportError


class UploadDownloaderTests(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
        self.url = os.environ.get("VIDEO_HTML_PAGE", "")
        self.invalid_url = os.environ.get("INVALID_HTML_PAGE", "")
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.downloader = UploadDownloader(self.url, self.dir_path)
        self.downloader_invalid = UploadDownloader(self.invalid_url, self.dir_path)

    def test_source(self):
        self.assertTrue(self.downloader.download(download=False))
        self.assertTrue(self.downloader.sources.endswith(".mp4"))
        self.assertRaises(LinkIsDown, self.downloader_invalid.download, download=False)
        self.assertFalse(self.downloader_invalid.sources.endswith(".mp4"))

    def test_poster(self):
        self.assertTrue(self.downloader.download(download=False))
        self.assertTrue(self.downloader.poster.endswith(".jpg") or self.downloader.poster.endswith(".png"))
        self.assertRaises(LinkIsDown, self.downloader_invalid.download, download=False)
        self.assertFalse(len(self.downloader_invalid.poster))

    def test_title(self):
        self.assertTrue(self.downloader.download(download=False))
        self.assertTrue(len(self.downloader.title))
        self.assertRaises(LinkIsDown, self.downloader_invalid.download, download=False)
        self.assertFalse(len(self.downloader_invalid.title))

    def test_name(self):
        done_name: str = "embed-xcehavjh1zy4.mp4"
        self.assertTrue(self.downloader.download(download=False))
        self.assertEqual(done_name, self.downloader.name)
        self.assertRaises(LinkIsDown, self.downloader_invalid.download, download=False)
        invalid_name: str = "embed-7upupztir1bv.mp4"
        self.assertEqual(invalid_name, self.downloader_invalid.name)

    def test_parser(self):
        self.assertIsInstance(self.downloader._parser(), str)
        self.assertTrue(len(self.downloader._data))
        self.assertRaises(LinkIsDown, self.downloader_invalid._parser)

    def test_clean(self):
        self.assertTrue(self.downloader.download(download=True))
        self.assertTrue(Utils.exist(self.downloader.output))
        self.downloader.clean()
        self.assertFalse(Utils.exist(self.downloader.output))
        self.assertRaises(LinkIsDown, self.downloader_invalid.download, download=False)
        self.assertFalse(Utils.exist(self.downloader_invalid.output))

    def test_download(self):
        self.assertTrue(self.downloader.download(download=False))
        self.assertRaises(LinkIsDown, self.downloader_invalid.download, download=False)
