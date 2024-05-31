import logging

from sentiment_analysis_model.config.core import PACKAGE_ROOT, AppConfig


# logging.getLogger(AppConfig.model.name).addHandler(logging.NullHandler())


with open(PACKAGE_ROOT / "VERSION") as version_file:
    __version__ = version_file.read().strip()