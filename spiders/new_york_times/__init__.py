from spiders.new_york_times.extract import NewYorkTimesExtractor
from spiders.new_york_times.parse import NewYorkTimesParser
from spiders.new_york_times.spider import NewYorkTimesSpider

new_york_times_spider = NewYorkTimesSpider(
    NewYorkTimesExtractor(), NewYorkTimesParser()
)
