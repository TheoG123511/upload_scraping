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
        self.invalid_url = os.environ.get("INVALID_HTML_PAGE", "")
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def test_download(self):
        pass

    def test_download_file(self):
        pass

    def test_about(self):
        pass
