# Original article
# https://blog.loadero.com/2022/01/20/test-automation-with-python/


def test_on_loadero(driver: TestUIDriver) -> None:
    # Opens the search engine DuckDuckGo with default search query of
    # google.com
    driver.navigate_to("https://duckduckgo.com/?q=google.com")

    # Locates an element with a CSS selector that is pointing to the first
    # search results title, waits for the element to become visible and clicks
    # on it.
    driver.e("css", "#r1-0 > div > h2").wait_until_visible().click()

    # Ensures that the web page has loaded before taking a screenshot.
    driver.e("css", "body > div:first-of-type").wait_until_visible()
    driver.save_screenshot("google.png")
