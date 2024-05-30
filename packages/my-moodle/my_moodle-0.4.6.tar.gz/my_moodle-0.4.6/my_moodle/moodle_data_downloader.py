"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
Moodle data downloader Class
"""

from .version import __version__


class MoodleDataDownloader:
    """Moodle data downloader"""

    def __init__(
        self,
        program_name: str,
        server: str,
        token: str,
        data_dir: str = "",
        enable_enrollment_download: bool = False,
        timeout: float = 300.0,
        rest_format: str = "json",
    ):
        pass

    @staticmethod
    def display_version() -> None:
        """Display the version"""
        print(f"Using my_moodle Version: {__version__}")

    def download_my_json_data(self) -> list[dict]:
        """Download my JSON data

        Returns:
            dict: A list of JSON courses
        """
        print("Download json data ...")
        return []

    def download_my_data(self) -> dict:
        """Download my data

        Returns:
            dict: The program JSON
        """
        print("Download my data - Updating")
        print("An error occurred. Please try again.")
        print("You can log a issue on GitHub.")
        print("https://github.com/marcocrowe/my-moodle-template/issues")
        return {}
