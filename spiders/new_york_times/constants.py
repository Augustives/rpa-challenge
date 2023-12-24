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
    "search_page_more_button": '//button[@data-testid="search-show-more-button"]',
    "news_image": '//div[@data-testid="photoviewer-children-Image"]/img',
    "tracker_button": '//button[@data-testid="expanded-dock-btn-selector"]',
}

CLASS_SELECTORS = {
    "news_date": "class:css-17ubb9w",
    "news_title": "class:css-2fgx4k",
    "news_description": "class:css-16nhkrn",
}
