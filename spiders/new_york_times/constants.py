BASE_URL = "https://www.nytimes.com/"

XPATHS = {
    "news_search_button": 'xpath://button[@data-testid="search-button"]',
    "news_search_input": 'xpath://input[@data-testid="search-input"]',
    "news_search_submit": 'xpath://button[@data-testid="search-submit"]',
    "categories_button": 'xpath://button[@data-testid="search-multiselect-button"]',
    "categories_select": '//ul[@data-testid="multi-select-dropdown-list"]/li/label/span[text()="{category}"]',
    "categories_spans": '//ul[@data-testid="multi-select-dropdown-list"]/li/label/span',
    "date_range_dropdown": 'xpath://button[@data-testid="search-date-dropdown-a"]',
    "date_range_button": 'xpath://button[@value="Specific Dates"]',
    "search_page_submit": 'xpath://button[@data-testid="search-page-submit"]',
    "search_page_sort": 'xpath://select[@data-testid="SearchForm-sortBy"]',
    "search_page_results": 'xpath://ol[@data-testid="search-results"]/li/div',
    "search_page_more_button": 'xpath://button[@data-testid="search-show-more-button"]',
    "index_header": 'xpath://a[@data-testid="site-index-header"]',
    "tracker_button": 'xpath://button[@data-testid="expanded-dock-btn-selector"]',
}
