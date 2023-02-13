#!/usr/bin/env python3
# -*- coding: utf8 -*-
try:
    import os
    from distutils.core import Command, setup
    from upload_scraping.src.config import Config
    from upload_scraping.src.version import __version__, __package__
except ImportError:
    raise ImportError

readme: str = ""
if os.path.exists('README.md'):
    readme_path = 'README.md'
    with open(readme_path, 'r') as f:
        readme = f.read()

# ========== Test package path =====
if not os.path.exists(__package__):
    packages: list = [os.path.join("src"),
                      os.path.join("test"),
                      os.path.join(r"src/utils"),
                      os.path.join(r"src/log")]
else:
    packages: list = [os.path.join(__package__, "src"),
                      os.path.join(__package__, "test"),
                      os.path.join(__package__, r"src/utils"),
                      os.path.join(__package__, r"src/log")]


# ========== Test command ==========
class TestEx(Command):
    description: str = "Running all unit test for upload_scrapping"
    user_options: list = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        import unittest
        suite = unittest.TestLoader().discover(Config.TEST_DIR)
        unittest.TextTestRunner(verbosity=2).run(suite)


setup(
    name=__package__,
    version=__version__,
    description='Scrapping video from upload player.',
    long_description=readme,
    keywords='python scraping',
    author='DAUP',
    author_email='',
    url='https://github.com/TheoG123511/upload_scraping',
    license="MIT license",
    package_data={
        __package__: [
            '../setup.py',
            '../README.md',
            '../LICENSE',
            '__init__.py',
            'src/__init__.py',
            'test/__init__.py',
            'src/log/__init__.py',
            'src/utils/__init__.py',
            'src/config.py',
            'src/upload_downloader.py',
            'src/exceptions.py',
            'src/version.py',
            'src/utils/colors.py',
            'src/utils/singleton.py',
            'src/utils/utils.py',
            'src/log/log.py',
            'test/test_upload_downloader.py',
            'test/test_upload_video_downloader.py',
            'test/link.txt'
        ]
    },
    cmdclass={
        "test": TestEx,
    },
    scripts=[
        'upload_video_downloader.py',
    ],

    packages=[
        __package__
    ],
    package_dir={
        'upload_scraping': 'upload_scraping',
    },
    classifiers=[
        'Environment :: Console',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT license',
    ],
)
