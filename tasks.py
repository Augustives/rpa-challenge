from robocorp.tasks import task
from spiders.new_york_times.spider import run_spider


@task
def new_york_times_task():
    run_spider()
