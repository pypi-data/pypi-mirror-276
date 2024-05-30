"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
Moodle data downloader package.
"""

# noinspection PyPep8Naming
from . import api_functions as ApiFunctions
# noinspection PyPep8Naming
from . import config_utility as ConfigUtility
# noinspection PyPep8Naming
from . import csv_utility as CsvUtility
# noinspection PyPep8Naming
from . import data_utility as DataUtility
# noinspection PyPep8Naming
from . import json_utility as JsonUtility
from . import markdown_methods
# noinspection PyPep8Naming
from . import notebook_utility as NotebookUtility
from .course_status import CourseStatus
from .moodle_data_downloader import MoodleDataDownloader
from .update_utility import update_my_moodle_template
from .version import __version__
from .__main__ import main

__all__ = [
    "ApiFunctions",
    "ConfigUtility",
    "CourseStatus",
    "CsvUtility",
    "DataUtility",
    "JsonUtility",
    "main",
    "markdown_methods",
    "MoodleDataDownloader",
    "NotebookUtility",
    "update_my_moodle_template",
    "__version__",
]
