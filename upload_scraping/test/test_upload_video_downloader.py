try:
    import os
    import unittest
    from dotenv import load_dotenv
except ImportError:
    raise ImportError


class UploadVideoDownloaderAppTests(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
        self.url = os.environ.get("VIDEO_HTML_PAGE", "")

    def test_download(self):
        pass

    def test_download_file(self):
        pass

    def test_about(self):
        pass
