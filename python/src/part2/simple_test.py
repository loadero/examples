# simple_test.py

import time
from testui.support.appium_driver import NewDriver

driver = NewDriver().set_logger().set_browser("chrome").set_selenium_driver()

driver.navigate_to("https://loadero.com/")
time.sleep(10)

driver.quit()
