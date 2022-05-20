# Original article https://blog.loadero.com/2022/05/19/local-tests-with-selenium-and-python-browser-automation/

def test_on_loadero(driver: TestUIDriver) -> None:    
    driver.navigate_to("https://loadero.com/")
    time.sleep(10)
