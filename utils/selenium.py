from RPA.Browser.Selenium import Selenium
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement


class SeleniumBrowser:
    def __init__(
        self, selenium_settings: dict = {}, browser_settings: dict = {}
    ):
        self._selenium_settings: dict = {
            "timeout": 5,
            "implicit_wait": 10,
        } | selenium_settings

        self._browser: Selenium = None
        self._browser_settings: dict = {"headless": True} | browser_settings

    def __enter__(self):
        self._browser = Selenium(**self._selenium_settings)
        self._browser.open_available_browser(**self._browser_settings)
        self._browser.maximize_browser_window()
        return self._browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._browser:
            self._browser.close_browser()


def wait_for_element_and_retrieve(
    browser: Selenium, locator: str | WebElement,
    multiple: bool = False, timeout: int = 10,
) -> WebElement:
    browser.wait_until_element_is_visible(locator, timeout=timeout)

    if multiple:
        result = browser.get_webelements(locator)
    else:
        result = browser.get_webelement(locator)

    return result


def wait_for_element_and_click(
    browser: Selenium, locator: str | WebElement, timeout: int = 10,
) -> WebElement:
    element = wait_for_element_and_retrieve(browser, locator, timeout=timeout)
    browser.click_element(element)

    return element


def wait_for_element_stale(old_elements):
    def _predicate(driver):
        try:
            return all(
                [not element.is_displayed() for element in old_elements]
            )
        except StaleElementReferenceException:
            return True

    return _predicate
