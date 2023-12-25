from datetime import datetime, timedelta

from RPA.Browser.Selenium import Selenium

from spiders.new_york_times.constants import XPATH_SELECTORS
from utils.selenium import wait_for_element_and_click


def get_date_range(months_ago: int) -> tuple[datetime, datetime]:
    """
    Calculates a date range extending back a specified number of months from today.
    """
    months_ago = max(1, int(months_ago))

    today = datetime.now().date()

    if months_ago == 1:
        date_since = today.replace(day=1)
    else:
        days_to_subtract = (months_ago - 1) * 30 + 1
        date_since = (today.replace(day=1) - timedelta(days=days_to_subtract)).replace(
            day=1
        )

    return today, date_since


def treat_date_str_edge_cases(date_str: str) -> datetime:
    """
    Treats some edge cases that happen in the date strings
    that are retrieved from the website.
    """
    if "Sept." in date_str:
        date_str = date_str.replace("Sept.", "Sep.")

    return date_str


def parse_date(date_str: str) -> datetime:
    """
    Receives a date string from the website and transforms it in
    a datetime object, via the know formats.
    """
    date_str = treat_date_str_edge_cases(date_str)

    # Formats that include the year
    formats_with_year = ["%b. %d, %Y", "%B %d, %Y"]
    for date_format in formats_with_year:
        try:
            return datetime.strptime(date_str, date_format).date()
        except ValueError:
            continue

    # Formats that don't include the year
    formats_without_year = ["%b. %d", "%B %d"]
    current_year = datetime.now().year
    for date_format in formats_without_year:
        try:
            parsed_date = datetime.strptime(date_str, date_format).date()
            parsed_date = parsed_date.replace(year=current_year)
            return parsed_date
        except ValueError:
            continue

    raise ValueError(f"Date format for '{date_str}' is not currently supported.")


def check_and_close_tracker(browser: Selenium):
    try:
        wait_for_element_and_click(browser, XPATH_SELECTORS["tracker_button"])
    except Exception:
        pass
