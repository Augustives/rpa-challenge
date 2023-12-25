from RPA.Browser.Selenium import Selenium

from spiders.new_york_times.extract import NewYorkTimesExtractor
from spiders.new_york_times.parse import NewYorkTimesParser
from utils.selenium import SeleniumBrowser
from utils.spider import BaseSeleniumSpider


class NewYorkTimesSpider(BaseSeleniumSpider):
    def __init__(self, extractor: NewYorkTimesExtractor, parser: NewYorkTimesParser):
        super().__init__(extractor, parser)

    def crawl(self):
        with SeleniumBrowser() as browser:
            data = self._extractor.extract(browser)
            self._parser.parse(data)
