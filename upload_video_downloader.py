#!/usr/bin/python3
# -*- coding: utf8 -*-
try:
    import sys
    import os
    import argparse
    import time
    from upload_scraping.src.exceptions import UploadVideoDownloaderAppError, StatusCode, LogWriteError, LinkIsNotValid
    from upload_scraping.src.utils.utils import Utils
    from upload_scraping.src.upload_downloader import UploadDownloader
    from upload_scraping.src.log.log import Logging
except ImportError:
    raise ImportError


class UploadVideoDownloaderApp(object):

    _TEST_MODE: bool = bool(os.environ.get("DEBUG", 0))
    _EXIT_CODE: int = 0
    _TIMEOUT: int = .666
    _MAX_THREAD: int = 2
    _DONE: str = "done_download"
    _DOWNLOAD_EX: str = "downloader_except"

    def __init__(self, parsing: bool = True) -> None:
        self._log: Logging = Logging()
        self.verbose: bool = False
        self.history: list = []
        self._counter: int = 0
        self.stats: dict = {self._DONE: 0, self._DOWNLOAD_EX: 0}
        if parsing:
            self.parse_arg()

    @staticmethod
    def color() -> None:
        # if os.name == "nt":
        #    os.system("color 7")
        pass

    @staticmethod
    def parse_file(path: str) -> list or Exception:
        if not Utils.exist(path):
            raise FileNotFoundError("%s not found" % path)
        try:
            with open(path, "r", encoding="utf8") as _:
                data = _.read()
        except (PermissionError, OSError, UnicodeEncodeError) as err:
            raise err
        return data.split("\n")

    def parse_arg(self) -> None:
        parser = argparse.ArgumentParser(description='Downloader for upload player by DAUP')
        subparsers = parser.add_subparsers()
        # download
        download_args = subparsers.add_parser(
            'download', help='download video from html page or iframe', aliases=['d']
        )
        download_args.add_argument(
            '-s',
            '--source',
            dest='source',
            default=str(),
            help='page or iframe url or config file',
            required=True
        )
        download_args.add_argument(
            '-o',
            '--output',
            dest='output',
            default=str(),
            help='output directory',
            required=False
        )
        download_args.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
        download_args.set_defaults(func=self.download)
        # about
        about_args = subparsers.add_parser('about', help='getting information about video', aliases=['a'])
        about_args.add_argument(
            '-s',
            '--source',
            dest='source',
            default=str(),
            help='page or iframe url',
            required=True
        )
        about_args.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
        about_args.set_defaults(func=self.about)

    def download(self, args) -> None:
        self.history = []
        if args.output:
            if Utils.exist(args.output) and not Utils.is_directory(args.output):
                raise UploadVideoDownloaderAppError("%s must be a directory" % args.source)
            elif not Utils.exist(args.output):
                Utils.create_directory(args.output)
        output = os.path.join(os.path.dirname(os.path.realpath(__file__)), "output")
        if not Utils.exist(args.source) and Utils.is_valid(args.source):
            self._process_download(args.source, args.output if args.output else output)
        elif Utils.exist(args.source):
            self._file_download(args.source, args.output if args.output else output)
        elif not Utils.is_valid(args.source):
            raise UploadVideoDownloaderAppError("%s is not valid url !" % args.source)

    def about(self, args) -> None:
        pass

    def _file_download(self, path: str, output_dir: str) -> None:
        for link in self.parse_file(path):
            try:
                if not len(link):
                    continue
                self._waiting()
                self._run(link, output_dir, from_file=True)
            except KeyboardInterrupt:
                self._print_exit()
                break
        self._waiting_download(from_file=True), self._print_exit(by_user=False)

    @Utils.run_in_thread
    def _run(self, url: str, output_dir: str, from_file: bool = False) -> None:
        try:
            self._counter += 1
            self._process_download(url, output_dir, from_file=from_file)
            self._counter -= 1
        except KeyboardInterrupt:
            raise KeyboardInterrupt

    def _process_download(self, url: str, output_dir: str, from_file: bool = False) -> None:
        downloader = None
        try:
            if url in self.history:
                return self._write_log("Duplicate link %s" % url) if self.verbose else None
            downloader = UploadDownloader(url, output_dir, verbose=self.verbose)
            downloader.download()
        except (StatusCode, LinkIsNotValid, LogWriteError) as _err:
            self._error(url, str(_err)), downloader.clean()
        except KeyboardInterrupt:
            if downloader:
                downloader.clean()
            if len(self.history):
                self._write_log("Stopped at %s" % self.history[-1])
            self._print_exit()
            self.color(), sys.exit(self._EXIT_CODE)
        self.stats[self._DONE] += 1
        if not from_file:
            self._waiting_download(from_file=False), self._print_exit(by_user=False)

    def _write_log(self, message: str) -> None:
        self._log.write_log(self, message)

    def _error(self, url: str, _exception: str) -> None:
        self.stats[self._DOWNLOAD_EX] += 1
        self._write_log("Downloader exception on %s message: %s" % (url, _exception))

    def _print_exit(self, by_user: bool = True) -> None:
        done = self.stats.get(self._DONE)
        except_count = self.stats.get(self._DOWNLOAD_EX)
        if self.verbose:
            if except_count > 0:
                self._write_log("Number of exception: %s" % except_count)
            self._write_log("Number of task done: %s" % (done - except_count))
        elif done > 0 and not self.verbose:
            self._write_log("Number of task done: %s" % (done - except_count))
        if by_user:
            self._write_log("Stop script by user. Exiting ...")

    def _waiting_download(self, from_file: bool = True) -> None:
        try:
            if from_file:
                while self._counter > 0:
                    time.sleep(self._TIMEOUT)
        except KeyboardInterrupt:
            pass

    def _waiting(self) -> None:
        while self._counter >= self._MAX_THREAD:
            time.sleep(self._TIMEOUT)


if __name__ == '__main__':
    UploadVideoDownloaderApp()
