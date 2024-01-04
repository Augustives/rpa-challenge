import re

from RPA.Browser.Selenium import Selenium

from new_york_times.constants import XPATH_SELECTORS
from utils.selenium import wait_for_element_and_retrieve


def validate_categories(browser: Selenium, categories: list[str]):
    categories_span_elements = wait_for_element_and_retrieve(
        browser,
        XPATH_SELECTORS["categories_spans"],
        multiple=True,
    )

    regex_pattern = r"^[A-Za-z]+"
    available_categories = [
        re.match(regex_pattern, category).group(0)
        if re.match(regex_pattern, category)
        else category
        for category in [element.text for element in categories_span_elements]
    ]

    for category in categories:
        if category not in available_categories:
            raise ValueError(
                f"Category '{category}' not found in available "
                f"options: {available_categories}."
            )
