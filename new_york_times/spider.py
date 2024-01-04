from new_york_times.extract import NewYorkTimesExtractor
from new_york_times.parse import NewYorkTimesParser
from utils.selenium import SeleniumBrowser


class NewYorkTimesSpider():
    def crawl(self):
        with SeleniumBrowser() as browser:
            data = NewYorkTimesExtractor(browser).extract()

            if data:
                NewYorkTimesParser().parse(data)
