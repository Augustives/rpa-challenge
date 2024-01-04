from robocorp.tasks import task

from new_york_times.extract import NewYorkTimesExtractor
from new_york_times.parse import NewYorkTimesParser
from utils.selenium import SeleniumBrowser


@task
def new_york_times_task():
    with SeleniumBrowser() as browser:
        data = NewYorkTimesExtractor(browser).extract()

        if data:
            NewYorkTimesParser().parse(data)
