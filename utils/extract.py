from abc import ABC, abstractmethod

from RPA.Browser.Selenium import Selenium


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self):
        pass


class BaseSeleniumExtractor(BaseExtractor):
    @abstractmethod
    def extract(self, browser: Selenium):
        pass
