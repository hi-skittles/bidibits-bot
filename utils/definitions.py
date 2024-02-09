import re
from typing import Any


class Customs:
    @staticmethod
    def has_twitter_link(url: str) -> tuple[bool, str | Any, str | Any] | bool:
        """
        Checks if the given URL or string is/contains a Twitter link.

        :param url: The URL to check.
        :return: True if the URL is a Twitter link, False otherwise.
        """
        twitter_regex = re.compile(r'https?://twitter\.com/(\w+)/status/(\d+)')
        # r"(https?:\/\/)?(www\.)?twitter\.com\/([a-zA-Z0-9_]+)\/status\/([0-9]+)"

        match = twitter_regex.search(url)

        if match:
            return True, match.group(1), match.group(2)
        else:
            return False, None, None


class Statics:
    @staticmethod
    def get_version_from_file(version_file: str = "./version") -> str:
        """
        Retrieves the version from the version file.

        :return: The version.
        """
        with open(version_file, "r") as file:
            return file.read().strip()
