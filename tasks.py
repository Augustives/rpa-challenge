from robocorp.tasks import task

from new_york_times.spider import NewYorkTimesSpider


@task
def new_york_times_task():
    NewYorkTimesSpider().crawl()
