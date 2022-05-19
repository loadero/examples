# loadero_script.py

import pytest
import time
from testui.support.appium_driver import NewDriver
from testui.support.testui_driver import TestUIDriver


@pytest.fixture(autouse=True)
def driver() -> TestUIDriver:    
    driver = (
        NewDriver()
        .set_logger()
        .set_browser("chrome")
        .set_selenium_driver()
    )
    
    print("starting test script execution")
    yield driver
    print("test script execution finished")

    driver.quit()


@pytest.mark.test
def test_on_loadero(driver: TestUIDriver) -> None:    
    driver.navigate_to("https://loadero.com/")
    time.sleep(10)
