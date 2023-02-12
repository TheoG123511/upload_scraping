try:
    import os
    import unittest
    from dotenv import load_dotenv
except ImportError:
    raise ImportError


class UploadDownloaderTests(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
        self.url = os.environ.get("VIDEO_HTML_PAGE", "")

    def test_name(self):
        pass

    def test_parser(self):
        pass

    def test_clean(self):
        pass

    def test_download(self):
        pass
