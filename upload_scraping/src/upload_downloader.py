#!/usr/bin/python3
# -*- coding: utf8 -*-
try:
    import copy
    import urllib3
    import requests
    import slimit
    from slimit import ast
    from slimit.parser import Parser
    from slimit.visitors import nodevisitor
    from bs4 import BeautifulSoup
    from urllib.parse import urlparse
    from upload_scraping.src.utils.utils import Utils
    from upload_scraping.src.log.log import Logging
    from exceptions import LinkIsNotValid, StatusCode, LinkIsDown
except ImportError:
    raise ImportError


class UploadDownloader:

    _DONE: int = 200
    _TIMEOUT: int = 30
    _MINIMAL_SIZE: int = 10
    BUFFER_SIZE: int = 5242880  # 5 mo
    ENCODING: str = "utf8"
    _PARSER: str = "html.parser"
    _VIDEO_ASK: str = "v.mp4"

    def __init__(self, url: str, output: str, verbose: bool = False, proxy: dict or None = None) -> None:
        self.url: str = url
        self.verbose: bool = verbose
        self.domain = urlparse(self.url)
        self.proxy: dict or None = proxy
        self._log: Logging = Logging()
        if not len(self.domain.netloc) or not self.url.endswith(".html"):
            raise LinkIsNotValid('%s is not valid url !' % self.url)
        self.output: str = Utils.create_path(output, self.name)

    @property
    def name(self) -> str:
        return self.url.split("/")[-1].replace(".html", ".mp4")

    def _parser(self) -> str:
        _headers = copy.copy(Utils.UPLOAD_GET_HEADERS)
        _headers["Referer"] = "https://%s/" % self.domain.netloc
        _r = requests.get(self.url, headers=_headers, timeout=self._TIMEOUT, proxies=self.proxy)
        if _r.status_code != self._DONE:
            raise StatusCode("Bad status code %s" % _r.status_code)
        soup = BeautifulSoup(_r.content.decode(self.ENCODING), self._PARSER)
        scripts = soup.find_all("script")
        field = {}
        for script in scripts:
            html_tags = script.text
            if self._VIDEO_ASK in html_tags:
                parser = Parser()
                tree = parser.parse(script.text)
                for node in nodevisitor.visit(tree):
                    if isinstance(node, ast.Assign):
                        _name: str = getattr(node.left, 'value', '')
                        if isinstance(node.right, ast.Array):
                            _list: list = []
                            for item in node.right:
                                _list.append(getattr(item, "value", ""))
                            field[_name] = _list
                        else:
                            field[_name] = getattr(node.right, 'value', '')
                break
        if not len(field):
            raise LinkIsDown("%s link is down !" % self.url)
        return str(field.get("sources")[0][1:-1])

    def clean(self) -> None:
        if Utils.exist(self.output):
            Utils.delete(self.output)

    @Utils.run_in_thread
    def run(self) -> None:
        self.download()

    def download(self, restart: bool = False) -> bool:
        counter: int = 0
        if Utils.exist(self.output) and not restart:
            return True
        self.clean()
        try:
            _link = self._parser()
        except (LinkIsDown, StatusCode) as err:
            self._write_log("Exception %s" % err), self.clean()
            return False
        domain = urlparse(_link)
        _headers = copy.copy(Utils.UPLOAD_VIDEO_HEADERS)
        _headers["Host"] = "%s" % domain.netloc
        _headers["Referer"] = "https://%s/" % self.domain.netloc
        _r = requests.get(_link, headers=_headers, stream=True, proxies=self.proxy)
        if _r.status_code != self._DONE:
            raise StatusCode("Bad status code %s" % _r.status_code)
        try:
            with open(self.output, "wb") as w:
                for chunk in _r.raw.stream(self.BUFFER_SIZE, decode_content=False):
                    if chunk:
                        if self.verbose:
                            self._write_log("write %s bytes" % self.BUFFER_SIZE)
                        w.write(chunk)
                        counter += 1
        except urllib3.exceptions.ProtocolError:
            self._write_log("Protocol error ! restart download ...")
            return self.download(restart=True)
        except OSError as err:
            self._write_log("Exception: %s" % err), Utils.delete(self.output), exit(666)
        if counter <= self._MINIMAL_SIZE:
            Utils.delete(self.output), self._write_log("Video is invalid at %s" % self.url)
        if Utils.exist(self.output):
            self._write_log("File save at %s" % self.output)
        return True

    def _write_log(self, message: str) -> None:
        self._log.write_log(self, message)


if __name__ == '__main__':
    # "https://uqload.co/embed-xcehavjh1zy4.html"

    path = r"F:/movie/game-of-thrones/saison1"
    path_link = r"F:/movie/game-of-thrones/saison1/link.txt"
    with open(path_link, "r", encoding=UploadDownloader.ENCODING) as r:
        data = r.read()
    data = data.split("\n")
    for link in data:
        if not len(link):
            continue
        upload = UploadDownloader(link, path)
        upload.download()

    path = r"F:/movie/game-of-thrones/saison2"
    path_link = r"F:/movie/game-of-thrones/saison2/link.txt"
    with open(path_link, "r", encoding=UploadDownloader.ENCODING) as r:
        data = r.read()
    data = data.split("\n")
    for link in data:
        if not len(link):
            continue
        upload = UploadDownloader(link, path)
        upload.download()

    path = r"F:/movie/game-of-thrones/saison3"
    path_link = r"F:/movie/game-of-thrones/saison3/link.txt"
    with open(path_link, "r", encoding=UploadDownloader.ENCODING) as r:
        data = r.read()
    data = data.split("\n")
    for link in data:
        if not len(link):
            continue
        upload = UploadDownloader(link, path)
        upload.download()

    path = r"F:/movie/game-of-thrones/saison4"
    path_link = r"F:/movie/game-of-thrones/saison4/link.txt"
    with open(path_link, "r", encoding=UploadDownloader.ENCODING) as r:
        data = r.read()
    data = data.split("\n")
    for link in data:
        if not len(link):
            continue
        upload = UploadDownloader(link, path)
        upload.download()

    path = r"F:/movie/game-of-thrones/saison5"
    path_link = r"F:/movie/game-of-thrones/saison5/link.txt"
    with open(path_link, "r", encoding=UploadDownloader.ENCODING) as r:
        data = r.read()
    data = data.split("\n")
    for link in data:
        if not len(link):
            continue
        upload = UploadDownloader(link, path)
        upload.download()

    path = r"F:/movie/game-of-thrones/saison6"
    path_link = r"F:/movie/game-of-thrones/saison6/link.txt"
    with open(path_link, "r", encoding=UploadDownloader.ENCODING) as r:
        data = r.read()
    data = data.split("\n")
    for link in data:
        if not len(link):
            continue
        upload = UploadDownloader(link, path)
        upload.download()

    path = r"F:/movie/game-of-thrones/saison7"
    path_link = r"F:/movie/game-of-thrones/saison7/link.txt"
    with open(path_link, "r", encoding=UploadDownloader.ENCODING) as r:
        data = r.read()
    data = data.split("\n")
    for link in data:
        if not len(link):
            continue
        upload = UploadDownloader(link, path)
        upload.download()

    path = r"F:/movie/game-of-thrones/saison8"
    path_link = r"F:/movie/game-of-thrones/saison8/link.txt"
    with open(path_link, "r", encoding=UploadDownloader.ENCODING) as r:
        data = r.read()
    data = data.split("\n")
    for link in data:
        if not len(link):
            continue
        upload = UploadDownloader(link, path)
        upload.download()
