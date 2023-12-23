from datetime import datetime

from RPA.Browser.Selenium import Selenium

from spiders.new_york_times.constants import BASE_URL, XPATHS
from spiders.new_york_times.utils import get_date_range, parse_date
from spiders.new_york_times.validate import validate_categories
from utils.selenium import (
    SeleniumBrowser,
    wait_for_element_and_click,
    wait_for_element_and_retrieve,
)
from utils.work_items import get_work_items_variables

VARIABLES = get_work_items_variables()


def check_and_close_tracker(browser: Selenium):
    try:
        wait_for_element_and_click(browser, XPATHS["tracker_button"])
    except Exception:
        pass


def extract_news(browser: Selenium, date_to: datetime, date_since: datetime):
    valid_news = []
    last_element_date = datetime.now().date()

    while last_element_date >= date_since:
        check_and_close_tracker(browser)
        wait_for_element_and_click(browser, XPATHS["search_page_more_button"])

        news_dates = wait_for_element_and_retrieve(
            browser, XPATHS["news_date"], multiple=True
        )
        news_titles = wait_for_element_and_retrieve(
            browser, XPATHS["news_title"], multiple=True
        )
        news_descriptions = wait_for_element_and_retrieve(
            browser, XPATHS["news_description"], multiple=True
        )

        last_element_date = parse_date(news_dates[-1].text)


def set_date_range(browser: Selenium, date_to: datetime, date_since: datetime):
    wait_for_element_and_click(browser, XPATHS["date_range_dropdown"])
    wait_for_element_and_click(browser, XPATHS["date_range_button"])

    browser.input_text("id:startDate", date_since.strftime("%m/%d/%Y"))
    browser.input_text("id:endDate", date_to.strftime("%m/%d/%Y"))

    wait_for_element_and_click(browser, XPATHS["date_range_dropdown"])


def set_categories(browser: Selenium):
    categories = VARIABLES.get("categories", [])

    if categories:
        wait_for_element_and_click(browser, XPATHS["categories_button"])

        validate_categories(browser, categories)

        for category in categories:
            wait_for_element_and_click(
                browser, XPATHS["categories_select"].format(category=category)
            )


def set_search_filters(browser: Selenium, date_to: datetime, date_since: datetime):
    set_categories(browser)
    set_date_range(browser, date_to, date_since)
    browser.select_from_list_by_value(XPATHS["search_page_sort"], "newest")


def follow_search_page(browser: Selenium):
    wait_for_element_and_click(browser, XPATHS["news_search_button"])
    browser.input_text(XPATHS["news_search_input"], VARIABLES.get("search_phrase", ""))
    wait_for_element_and_click(browser, XPATHS["news_search_submit"])


def follow_main_page(browser: Selenium):
    browser.go_to(BASE_URL)


def run_spider():
    with SeleniumBrowser(browser_settings={"browser": "chrome"}) as browser:
        browser.maximize_browser_window()

        follow_main_page(browser)
        follow_search_page(browser)

        date_to, date_since = get_date_range(VARIABLES.get("months", 0))
        set_search_filters(browser, date_to, date_since)

        extract_news(browser, date_to, date_since)

        print(123)
