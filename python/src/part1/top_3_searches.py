def test_on_loadero(driver: TestUIDriver) -> None:
    # The main logic of the test is in top_search_results function
    for result in top_search_results(driver, "loadero"):
        print(result)


def top_search_results(
    driver: TestUIDriver, search_query: str
) -> list[str]:
    # List of top 3 search results
    results = []

    def repeated_search(search_query: str):
        # Selectors for the search bar and search button change when a search
        # has been previously performed.
        search_bar = "#search_form_input"
        search_button = "#search_button"

        # Locates search bar element and verifies that it is present.
        search_bar_element = driver.e(
            "css", search_bar
        ).wait_until_visible()

        # Clears the previous search query and inputs the new one.
        search_bar_element.clear()
        search_bar_element.send_keys(search_query)

        # Clicks on the search button similar to the initial search it is not
        # necessary to verify the presence of this element.
        driver.e("css", search_button).click()

        repeated_search_results = (
            "Top 3 DuckDuckGo search "
            + f"results for {search_query} ->\n"
        )

        for i in range(3):
            # Creates a css selector that indicates to the search result title.
            selector = f"#r1-{i} > div > h2 > a.result__a"

            # Locates the search element and verifies that it is present.
            search_result_element = driver.e(
                "css", selector
            ).wait_until_visible()

            # Retrives the title of search result and adds it to result string.
            title = search_result_element.get_text()
            repeated_search_results += "\t" + title + "\n"

        results.append(repeated_search_results)

    # Selectors.
    home_page_search_bar = "#search_form_input_homepage"
    home_page_search_button = "#search_button_homepage"

    # Opens the search engine duckduckgo.
    driver.navigate_to("https://duckduckgo.com/")

    # Locates search bar, wait for the element to load and sends search query
    # to it
    driver.e(
        "css", home_page_search_bar
    ).wait_until_visible().send_keys(search_query)

    # Locates search button and clicks it. Notice that it is not necessary to
    # wait for the element to become visible because the test has already
    # verified that search bar was visible and search button is right next to
    # search bar
    driver.e("css", home_page_search_button).click()

    initial_result = (
        "Top 3 DuckDuckGo search "
        + f"results for {search_query} ->\n"
    )

    # Iterates over top 3 search results
    for i in range(3):
        # Creates a css selector that indicates to the search result title.
        selector = f"#r1-{i} > div > h2 > a.result__a"

        # Locates the search element and verifies that it is present.
        search_result_element = driver.e(
            "css", selector
        ).wait_until_visible()

        # Retrives the title of search result and adds it to result string.
        title = search_result_element.get_text()
        initial_result += "\t" + title + "\n"

        # Retrives the top 3 search results when searching for the results
        # title.
        repeated_search(title)

    results.append(initial_result)

    return results
