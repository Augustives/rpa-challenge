# flake8: noqa


BASE_URL = "https://www.nytimes.com/"

XPATH_SELECTORS = {
    "news_search_button": '//button[@data-testid="search-button"]',
    "news_search_input": '//input[@data-testid="search-input"]',
    "news_search_submit": '//button[@data-testid="search-submit"]',
    "categories_button": '//button[@data-testid="search-multiselect-button"]',
    "categories_spans": '//label[@data-testid="DropdownLabel"]/span',
    "categories_select": '//label[@data-testid="DropdownLabel"]/span[text()="{category}"]',
    "date_range_dropdown": '//button[@data-testid="search-date-dropdown-a"]',
    "date_range_button": '//button[@value="Specific Dates"]',
    "search_page_submit": '//button[@data-testid="search-page-submit"]',
    "search_page_sort": '//select[@data-testid="SearchForm-sortBy"]',
    "search_page_results": '//ol[@data-testid="search-results"]',
    "tracker_button": '//button[@data-testid="expanded-dock-btn-selector"]',
}

CLASS_SELECTORS = {
    "news_containers": 'css-1l4w6pd',
    "news_title": "css-2fgx4k",
    "news_date": "css-17ubb9w",
    "news_description": "css-16nhkrn",
    "news_image_src": "css-rq4mmj"
}
