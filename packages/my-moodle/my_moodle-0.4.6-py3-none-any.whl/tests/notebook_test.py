"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
Main module to run the program
"""

try: # Ensure the my_moodle package is installed
    from my_moodle import NotebookUtility
except ImportError:
    print("my_moodle is not installed. Installing now...")
    #%pip install my_moodle
    from my_moodle import NotebookUtility

NotebookUtility.display_jupyter_notebook_header(
    github_username="marcocrowe",  # TODO: Change this to your GitHub username
    repository="my-moodle-template",  # TODO: Change this to your repository name
)

from os import getcwd
#from IPython.display import Markdown
from my_moodle import ConfigUtility, CourseStatus, DataUtility, MoodleDataDownloader

MoodleDataDownloader.display_version()
program, server, token = ConfigUtility.check_and_read_config()
moodle_data_downloader = MoodleDataDownloader(program, server, token, getcwd())

courses: list = moodle_data_downloader.download_my_json_data()
active_courses: list = DataUtility.get_courses_by_status(courses, CourseStatus.ACTIVE)
favourite_courses: list = DataUtility.get_courses_favoured(courses)

(("### All Courses"))
(DataUtility.courses_json_to_html(courses))
(("### Active Courses"))
(DataUtility.courses_json_to_html(active_courses))
(("### Favourite Courses"))
(DataUtility.courses_json_to_html(favourite_courses))

_ = moodle_data_downloader.download_my_data()
