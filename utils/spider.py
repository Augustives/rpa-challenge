from abc import ABC, abstractmethod

from utils.extract import BaseSeleniumExtractor
from utils.parse import BaseParser


class BaseSeleniumSpider(ABC):
    def __init__(self, extractor: BaseSeleniumExtractor, parser: BaseParser):
        self._extractor = extractor
        self._parser = parser

    @abstractmethod
    def crawl(self):
        pass
