import logging
from datetime import datetime

from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from selenium.webdriver.support.ui import WebDriverWait

from spiders.new_york_times.data import News
from spiders.new_york_times.constants import BASE_URL, XPATHS
from spiders.new_york_times.utils import (
    check_and_close_tracker,
    get_date_range,
    parse_date,
)
from spiders.new_york_times.validate import validate_categories
from utils.extract import BaseSeleniumExtractor
from utils.selenium import wait_for_element_and_click, wait_for_element_and_retrieve
from utils.spider import BaseSeleniumExtractor
from utils.work_items import get_input_work_item


class NewYorkTimesExtractor(BaseSeleniumExtractor):
    WORK_ITEM = get_input_work_item()
    VARIABLES = WORK_ITEM.payload

    def extract_news_images(self, data: list[News]):
        requests = HTTP()
        for news in data:
            file_name = f"{news.title}-image.jpg"
            requests.download(news.image_src, f"./output/{file_name}")
            news.image_file_name = file_name

    def expand_news_and_wait(self, browser: Selenium):
        current_news_count = len(
            wait_for_element_and_retrieve(browser, XPATHS["news_date"], multiple=True)
        )
        wait_for_element_and_click(browser, XPATHS["search_page_more_button"])
        WebDriverWait(browser, 10).until(
            lambda _: len(
                wait_for_element_and_retrieve(
                    browser, XPATHS["news_date"], multiple=True
                )
            )
            > current_news_count
        )

    def paginate_and_extract_news_data(
        self, browser: Selenium, date_since: datetime
    ) -> list[News]:
        last_element_date = datetime.now().date()
        news_data = []

        while last_element_date >= date_since:
            check_and_close_tracker(browser)
            self.expand_news_and_wait(browser)

            news_titles = [
                element.text
                for element in wait_for_element_and_retrieve(
                    browser, XPATHS["news_title"], multiple=True
                )
            ]
            news_descriptions = [
                element.text if element.text else ""
                for element in wait_for_element_and_retrieve(
                    browser, XPATHS["news_description"], multiple=True
                )
            ]
            news_dates = [
                parse_date(element.text)
                for element in wait_for_element_and_retrieve(
                    browser, XPATHS["news_date"], multiple=True
                )
            ]
            news_images_src = [
                element.get_property("src")
                for element in wait_for_element_and_retrieve(
                    browser, XPATHS["news_image"], multiple=True
                )
            ]

            news_data.extend(
                zip(news_titles, news_descriptions, news_dates, news_images_src)
            )

            last_element_date = news_dates[-1]

        return [
            News(
                search_phrase=self.VARIABLES.get("search_phrase", ""),
                title=title,
                description=description,
                date=date,
                image_src=image_src,
            )
            for title, description, date, image_src in news_data
            if date >= date_since
        ]

    def extract_news(self, browser: Selenium, date_since: datetime) -> list[News]:
        try:
            news = self.paginate_and_extract_news_data(browser, date_since)
            self.extract_news_images(news)
        except AssertionError:
            logging.info("Found zero news for the given search phrase")
            return []

        return news

    def set_date_range(
        self, browser: Selenium, date_to: datetime, date_since: datetime
    ):
        wait_for_element_and_click(browser, XPATHS["date_range_dropdown"])
        wait_for_element_and_click(browser, XPATHS["date_range_button"])

        browser.input_text("id:startDate", date_since.strftime("%m/%d/%Y"))
        browser.input_text("id:endDate", date_to.strftime("%m/%d/%Y"))

        wait_for_element_and_click(browser, XPATHS["date_range_dropdown"])

    def set_categories(self, browser: Selenium):
        categories = self.VARIABLES.get("categories", [])

        if categories:
            wait_for_element_and_click(browser, XPATHS["categories_button"])

            validate_categories(browser, categories)

            for category in categories:
                wait_for_element_and_click(
                    browser, XPATHS["categories_select"].format(category=category)
                )

    def set_search_filters(
        self, browser: Selenium, date_to: datetime, date_since: datetime
    ):
        self.set_categories(browser)
        self.set_date_range(browser, date_to, date_since)
        browser.select_from_list_by_value(XPATHS["search_page_sort"], "newest")

    def follow_search_page(self, browser: Selenium):
        wait_for_element_and_click(browser, XPATHS["news_search_button"])
        browser.input_text(
            XPATHS["news_search_input"], self.VARIABLES.get("search_phrase", "")
        )
        wait_for_element_and_click(browser, XPATHS["news_search_submit"])

    def follow_main_page(self, browser: Selenium):
        browser.go_to(BASE_URL)

    def extract(self, browser: Selenium) -> list[News]:
        self.follow_main_page(browser)
        self.follow_search_page(browser)

        date_to, date_since = get_date_range(self.VARIABLES.get("months", 0))
        self.set_search_filters(browser, date_to, date_since)

        return self.extract_news(browser, date_since)
