try:
    import os
    from upload_scraping import test
    import upload_scraping.src.log as log
except ImportError:
    raise ImportError


class Config:
    _BASE_MODULE: str = "__init__.py"
    _BASE_MODULE_COMPILED: str = "__init__.pyc"
    TEST_DIR: str = os.path.normpath(
        test.__file__.replace(_BASE_MODULE_COMPILED, '').replace(_BASE_MODULE, '')
    )
    LOG_FILE_PATH: str = os.path.normpath(
        log.__file__.replace(_BASE_MODULE_COMPILED, 'activity.log').replace(_BASE_MODULE, 'activity.log')
    )
