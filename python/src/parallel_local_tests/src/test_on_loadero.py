import os
import sys
import time

import pytest
from selenium.webdriver.chrome.options import Options
from testui.support.appium_driver import NewDriver
from testui.support.testui_driver import TestUIDriver

from participant import Participant
from thread_with_return_value import ThreadWithReturnValue

REMOTE_URL = ""
PARTICIPANTS = 1
GLOBALS = []

participants_env = os.getenv('NUMBER_OF_PARTICIPANTS')
if participants_env is not None:
    PARTICIPANTS = int(participants_env)

timestamp = int(time.time())
for p in range(PARTICIPANTS):
    participant = Participant(timestamp)
    timestamp += 1
    GLOBALS.append(participant.participant_id)

selenium_url_env = os.getenv('SELENIUM_REMOTE_URL')
if selenium_url_env is not None:
    REMOTE_URL = selenium_url_env

# TestUIDriver
@pytest.fixture(autouse=True)
def driver() -> TestUIDriver:
    """Generator function that yields a list of TestUIDriver instances.

    This function creates a list of TestUIDriver instances, one for each participant
    specified by the PARTICIPANTS constant. The TestUIDriver instances are created using
    Selenium WebDriver with Chrome, and are configured with various options to enable
    media streams and other settings. If REMOTE_URL is specified, the drivers will be
    created using a remote URL instead of a local driver.

    Yields:
        A list of TestUIDriver instances.

    Raises:
        ValueError: If PARTICIPANTS is less than 1.
    """
    options = Options()
    chrome_options = ["no-sandbox", "use-fake-device-for-media-stream"]
    prefs = {
        "profile": {
            "content_settings": {
                "exceptions": {
                    "media_stream_camera": {"https://*,*": {"setting": 1}},
                    "media_stream_mic": {"https://*,*": {"setting": 1}},
                }
            },
        }
    }
    options.add_experimental_option("prefs", prefs)
    for o in chrome_options:
        options.add_argument(o)

    drivers = []
    for _ in range(PARTICIPANTS):
        if REMOTE_URL != "":
            driver = (
                NewDriver()
                .set_logger()
                .set_remote_url(REMOTE_URL)
                .set_browser("chrome")
                .set_selenium_driver(chrome_options=options)
            )
        else:
            driver = (
                NewDriver()
                .set_logger()
                .set_browser("chrome")
                .set_selenium_driver(chrome_options=options)
            )

        drivers.append(driver)

    yield drivers

    for participant_driver in drivers:
        participant_driver.quit()

# Parallel test execution
@pytest.mark.demotest
def test_on_loadero(driver: TestUIDriver) -> None:
    """Test function that runs Loadero tests for each participant.

    This function creates a list of threads, one for each driver in the driver list.
    Each thread runs the `test` function with a different participant ID, and returns
    the result code. If any of the threads return a non-zero status code, an exception
    is raised.

    Args:
        driver: A list of TestUIDriver instances.
    Raises:
        Exception: If any of the threads return a non-zero status code.
    """
    try:
        threads = []
        participant.participant_id = GLOBALS[0]
        for d in driver:
            participant.participant_id += 1
            t = ThreadWithReturnValue(target=test, args=(d, participant.participant_id, ))
            threads.append(t)
            print('Created thread: ', participant.participant_id)
            t.start()
        fail = False
        for t in threads:
            status = t.join()
            print(f'Finished thread: {participant.participant_id} With code: {status}')
            if status != 0:
                fail = True
        if fail is True:
            raise Exception('One of the participants failed')

    except Exception as main_exception:
        print(f'Exception Handled in Main, Details of the Exception: {main_exception}')
        sys.exit(-1)

# Test
def test(driver, participant_id):
    """
    Test the ability to join and remain in a video room using the specified WebDriver.

    Parameters:
        driver: A WebDriver instance representing the browser to use for testing.
        participant_id: An integer identifying the participant in the test.

    Returns:
        0 if the test passed successfully, or a non-zero value if an error occurred.
    """
    # room connect options
    url = 'https://janus.conf.meetecho.com/videoroomtest.html'
    identity = 'Participant' + str(participant_id)

    take = 2
    interval = 60
    element_timeout = 35

    # open webpage
    driver.navigate_to(url)
    driver.e('css', 'body').wait_until_visible(element_timeout)  # 35

    # join room
    driver.e('css', '#start').wait_until_visible(element_timeout)  # 35
    driver.e('css', '#start').click()
    driver.e('css', '#username').wait_until_visible(element_timeout)
    driver.e('css', '#username').send_keys(identity)
    driver.e('css', '#register').click()
    time.sleep(interval)

    # check if not Disconnected
    for _ in range(take):
        # page still loaded
        driver.e('css', 'body').wait_until_visible(element_timeout)  # 35s
        # participant not disconnected
        time.sleep(interval)  # 60s
        # disconect
        driver.e('css', '#start').wait_until_visible(element_timeout).click()
    pass
    return 0
