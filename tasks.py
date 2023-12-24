from robocorp.tasks import task

from spiders.new_york_times import new_york_times_spider


@task
def new_york_times_task():
    new_york_times_spider.crawl()
