"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
Config utility module
"""

def check_and_read_config(_: str = "config.ini") -> tuple[str, str, str]:
    """Check if the config file exists. If not, create it and
    then read and return the server and token config.

    Args:
        config_filepath (str): The config file path

    Returns:
        tuple[str, str, str]: A tuple containing the program name, server and token
    """
    program_name = "Course"
    server= "https://school.moodledemo.net"
    token="c010b64653af446db3f70e2b7b15fd1c"
    return program_name, server, token
