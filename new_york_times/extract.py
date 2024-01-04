import hashlib
from datetime import datetime
from pathlib import Path

from RPA.Browser.Selenium import By, Selenium
from RPA.HTTP import HTTP
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

from new_york_times.constants import BASE_URL, CLASS_SELECTORS, XPATH_SELECTORS
from new_york_times.data import News
from new_york_times.utils import (check_and_close_tracker, get_date_range,
                                  parse_date)
from new_york_times.validate import validate_categories
from utils.selenium import (wait_for_element_and_click,
                            wait_for_element_and_retrieve)
from utils.work_items import get_input_work_item


class NewYorkTimesExtractor():
    WORK_ITEM = get_input_work_item()
    VARIABLES = WORK_ITEM.payload

    def __init__(self, browser: Selenium):
        self._browser = browser

    def _load_news_results(self):
        current_news_count = len(
            wait_for_element_and_retrieve(
                self._browser,
                f'class:{CLASS_SELECTORS["news_containers"]}',
                multiple=True
            )
        )

        wait_for_element_and_click(
            self._browser, XPATH_SELECTORS["search_page_more_button"]
        )

        WebDriverWait(self._browser, 10).until(
            lambda _: len(
                wait_for_element_and_retrieve(
                    self._browser,
                    f'class:{CLASS_SELECTORS["news_containers"]}',
                    multiple=True
                )
            ) > current_news_count
        )

    def _extract_news_images(self, data: list[News]):
        requests = HTTP()
        output_directory = Path("./output")

        for news in data:
            if news.image_src:
                title_hash = hashlib.md5(news.title.encode()).hexdigest()
                file_name = f"{title_hash}.jpg"
                file_path = output_directory / file_name

                requests.download(news.image_src, str(file_path))
                news.image_file_name = file_name

    def _extract_news_data(self, date_since: datetime) -> list[News]:
        check_and_close_tracker(self._browser)
        self._load_news_results()

        news_containers = wait_for_element_and_retrieve(
            self._browser,
            XPATH_SELECTORS["search_page_results"]
        ).find_elements(By.CLASS_NAME, CLASS_SELECTORS['news_containers'])

        news_data = []
        for container in news_containers:
            date = wait_for_element_and_retrieve(
                self._browser, container.find_element(
                    By.CLASS_NAME, CLASS_SELECTORS["news_date"]
                )
            ).text

            date = parse_date(date)
            if date < date_since:
                continue

            title = wait_for_element_and_retrieve(
                self._browser, container.find_element(
                    By.CLASS_NAME, CLASS_SELECTORS["news_title"]
                )
            ).text

            try:
                description_element = container.find_element(
                    By.CLASS_NAME, CLASS_SELECTORS["news_description"]
                )
                description = wait_for_element_and_retrieve(
                    self._browser, description_element
                ).text
            except NoSuchElementException:
                description = ""

            try:
                image_src_element = container.find_element(
                    By.CLASS_NAME, CLASS_SELECTORS["news_image_src"]
                )
                image_src = wait_for_element_and_retrieve(
                    self._browser, image_src_element
                ).get_property("src")
            except NoSuchElementException:
                image_src = ""

            news_data.append(News(
                search_phrase=self.VARIABLES.get("search_phrase", ""),
                title=title,
                description=description,
                date=date,
                image_src=image_src
            ))

        return news_data

    def _extract_news(self, date_since: datetime) -> list[News]:
        news = self._extract_news_data(date_since)
        self._extract_news_images(news)

        return news

    def _set_date_range(self, date_to: datetime, date_since: datetime):
        wait_for_element_and_click(
            self._browser, XPATH_SELECTORS["date_range_dropdown"]
        )
        wait_for_element_and_click(
            self._browser, XPATH_SELECTORS["date_range_button"]
        )

        self._browser.input_text(
            "id:startDate", date_since.strftime("%m/%d/%Y")
        )
        self._browser.input_text("id:endDate", date_to.strftime("%m/%d/%Y"))

        wait_for_element_and_click(
            self._browser, XPATH_SELECTORS["date_range_dropdown"]
        )

    def _set_categories(self, categories: list[str]):
        wait_for_element_and_click(
            self._browser, XPATH_SELECTORS["categories_button"]
        )

        validate_categories(self._browser, categories)

        for category in categories:
            wait_for_element_and_click(
                self._browser,
                XPATH_SELECTORS["categories_select"].format(
                    category=category
                )
            )

    def _set_search_filters(self, date_to: datetime, date_since: datetime):
        categories = self.VARIABLES.get("categories", [])
        if categories:
            self._set_categories(categories)

        self._browser.select_from_list_by_value(
            XPATH_SELECTORS["search_page_sort"], "newest"
        )

        self._set_date_range(date_to, date_since)

    def _follow_search_page(self):
        wait_for_element_and_click(
            self._browser, XPATH_SELECTORS["news_search_button"]
        )

        self._browser.input_text(
            XPATH_SELECTORS["news_search_input"],
            self.VARIABLES.get("search_phrase", "")
        )

        wait_for_element_and_click(
            self._browser, XPATH_SELECTORS["news_search_submit"]
        )

    def _follow_main_page(self):
        self._browser.go_to(BASE_URL)

    def extract(self) -> list[News]:
        self._follow_main_page()
        self._follow_search_page()

        date_to, date_since = get_date_range(
            self.VARIABLES.get("months", 0)
        )
        self._set_search_filters(date_to, date_since)

        return self._extract_news(date_since)
