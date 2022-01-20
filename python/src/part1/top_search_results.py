def test_on_loadero(driver: TestUIDriver) -> None:
    # The main logic of the test is in top_search_results function
    print(top_search_results(driver, "loadero", 10))


# top_search_results returns the top n search results for search_query.
def top_search_results(driver: TestUIDriver, search_query: str, n: int) -> str:
    # Limits the search result count to 10, because a single search query in
    # DuckDuckGo search engine returns only 10 results.
    n = min(n, 10)

    # Selectors.
    home_page_search_bar = "#search_form_input_homepage"
    home_page_search_button = "#search_button_homepage"

    # Opens the search engine DuckDuckGo.
    driver.navigate_to("https://duckduckgo.com/")

    # Locates search bar, waits for the element to load and sends a search query
    # to it
    driver.e("css", home_page_search_bar).wait_until_visible().send_keys(
        search_query
    )

    # Locates search button, verifies that it is visible and clicks it.
    driver.e("css", home_page_search_button).wait_until_visible().click()

    result = f"Top {n} DuckDuckGo search results for {search_query} ->\n"

    # Iterates over top 3 search results
    for i in range(n):
        # Creates a css selector that indicates to the search result title.
        selector = f"#r1-{i} > div > h2 > a.result__a"

        # Locates the search element and verifies that it is present.
        search_result_element = driver.e("css", selector).wait_until_visible()

        # Retrives the title of search result and adds it to result string.
        title = search_result_element.get_text()
        result += f"\t {title} \n"

    return result
