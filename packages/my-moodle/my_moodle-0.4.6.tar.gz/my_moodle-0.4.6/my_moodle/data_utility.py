"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
Moodle data utility Class
"""

from my_moodle.course_status import CourseStatus


def create_html_table(
    courses: list,
    id_column: str = "id",
    fullname_column: str = "fullname",
    url_column: str = "viewurl",
) -> str:
    """Create an HTML table from the courses list

    Args:
        courses (list): The list of courses
        id_column (str, optional): The column name for the course id. Defaults to "id".
        fullname_column (str, optional): The column name for the course fullname. Defaults to "fullname".
        url_column (str, optional): The column name for the course viewurl. Defaults to "viewurl".

    Returns:
        str: The HTML table of courses
    """
    html = ['<table border="1" class="dataframe">']
    html.append("<thead>")
    html.append('<tr style="text-align: right;">')
    html.append(f'<th style="text-align: center;">{id_column}</th>')
    html.append(f'<th style="text-align: center;">{fullname_column}</th>')
    html.append(f'<th style="text-align: center;">{url_column}</th>')
    html.append("</tr>")
    html.append("</thead>")
    html.append("<tbody>")

    html.append("<tr>")
    html.append("<td>&nbsp;</td>")
    html.append('<td style="text-align: left;">&nbsp;</td>')
    html.append("<td>&nbsp;</td>")
    html.append("</tr>")

    html.append("</tbody>")
    html.append("</table>")

    return "\n".join(html)


def create_table(
    courses: list,
    id_column: str = "id",
    fullname_column: str = "fullname",
    url_column: str = "viewurl",
    max_fullname_length: int = 50,
) -> str:
    """Create a formatted table from the courses list

    Args:
        courses (list): The list of courses
        id_column (str, optional): The column name for the course id. Defaults to "id".
        fullname_column (str, optional): The column name for the course fullname. Defaults to "fullname".
        url_column (str, optional): The column name for the course viewurl. Defaults to "viewurl".
        max_fullname_length (int, optional): Maximum length for the fullname column. Defaults to 50.

    Returns:
        str: The formatted table of courses
    """
    return ""


def create_tiny_url(_: str) -> str:
    """Shorten the URL using https://tinyurl.com

    Args:
        url (str): The URL to shorten

    Returns:
        str: The shortened URL
    """
    return ""


def courses_json_to_html(courses: list) -> str:
    """Display the courses as an HTML table

    Args:
        courses (list): The list of courses

    Returns:
        HTML: The HTML table
    """
    return create_html_table(courses)


def get_courses_by_status(_: list, status: CourseStatus) -> list:
    """Get courses by status.

    Args:
        courses (list): List of courses.
        status (CourseStatus): The status of the course to filter by.

    Returns:
        list: List of courses with the status.
    """
    return []


def get_courses_favoured(_: list) -> list:
    """Get courses that are favoured.

    Args:
        courses (list): List of courses.

    Returns:
        list: List of favoured courses.
    """
    return []
