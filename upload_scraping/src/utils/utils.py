try:
    import os
    import secrets
    import requests
    import threading
    import subprocess
    import shutil
    import errno
    import stat
    import re
    from exceptions import StatusCode
except ImportError:
    raise ImportError


class Utils:
    UPLOAD_GET_HEADERS: dict = {
        "sec-ch-ua": '"Chromium";v="95", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "upgrade-insecure-requests": "1",
        "referer": "",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                      ' like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                  'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        "sec-fetch-dest": "iframe",
        "accept-encoding": "gzip, deflate",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    UPLOAD_VIDEO_HEADERS: dict = {
        "Host": "",
        "Sec-Ch-Ua": '"Chromium";v="109", "Not_A Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                      "537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "identity;q=1, *;q=0",
        "Referer": "",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "video",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive"
    }

    @staticmethod
    def create_path(_dir: str, _file_name: str) -> str:
        return os.path.normpath(os.path.join(_dir, _file_name))

    @staticmethod
    def delete(_path: str) -> None:
        if os.path.exists(_path):
            if os.path.isfile(_path):
                try:
                    os.chmod(_path, 0o777)
                    os.remove(_path)
                except (FileNotFoundError, OSError, PermissionError) as err:
                    raise err
            for root, dirs, files in os.walk(_path):
                for file in files:
                    filePath = os.path.join(root, file)
                    try:
                        os.chmod(filePath, 0o777)
                        os.remove(filePath)
                    except (FileNotFoundError, OSError, PermissionError):
                        continue
            shutil.rmtree(_path, ignore_errors=True, onerror=Utils.handleRemoveReadonly)

    @staticmethod
    def handleRemoveReadonly(func, path: str, exc):
        exc_value = exc[1]
        if func in (os.rmdir, os.remove) and exc_value.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
            func(path)
        else:
            raise

    @staticmethod
    def create_directory(directory_path: str) -> bool or Exception:
        if os.path.exists(directory_path):
            return True
        try:
            os.mkdir(directory_path)
        except (PermissionError, OSError, FileNotFoundError, FileExistsError) as err:
            raise err
        return True

    @staticmethod
    def exist(file_path: str) -> bool:
        return os.path.exists(file_path)

    @staticmethod
    def is_directory(path: str) -> bool:
        return os.path.isdir(path)

    @staticmethod
    def run_in_thread(function: any):
        def run(*k, **kw):
            t = threading.Thread(target=function, args=k, kwargs=kw, daemon=True)
            t.start()
            return t

        return run

    @staticmethod
    def is_valid(url: str) -> bool:
        regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url is not None and regex.search(url)

    @staticmethod
    def random(_min: int = 1, _max: int = 5) -> int:
        if _max < _min:
            return _max
        return secrets.choice([i for i in range(_min, _max + 1)])
