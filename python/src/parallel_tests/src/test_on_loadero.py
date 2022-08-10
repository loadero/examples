from testui.support.appium_driver import NewDriver
from testui.support.testui_driver import TestUIDriver
from testui.elements.testui_element import e
from selenium.webdriver.chrome.options import Options
from threading import Thread
from wsgiref.simple_server import demo_app
import time
import pytest
import sys
import os

remote_url = ""
participants = 1
GLOBALS = []

class Participant:
    def __init__(self, id):
        self.id = id

participants_env = os.getenv('NUMBER_OF_PARTICIPANTS')
if participants_env is not None:
    participants = int(participants_env) 

timestamp = time.time()
for p in range(participants):
    participant = Participant(timestamp)
    timestamp += 1
    GLOBALS.append(participant.id)

selenium_url_env = os.getenv('SELENIUM_REMOTE_URL')
if selenium_url_env is not None:
    remote_url = selenium_url_env

@pytest.fixture(autouse=True)
def driver() -> TestUIDriver:
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
    for d in range(participants):
        if remote_url != "":
            driver = (
            NewDriver()
                .set_logger()
                .set_remote_url(remote_url)
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

    for d in drivers:
        d.quit()

@pytest.mark.loaderotest
def test_on_loadero(driver: TestUIDriver) -> None: #parallel test
    class ThreadWithReturnValue(Thread):
        def __init__(self, group = None, target = None, name = None,
                    args = (), kwargs = {}, Verbose = None):
            Thread.__init__(self, group, target, name, args, kwargs)
            self._return = None
        def run(self):
            if self._target is not None:
                self._return = self._target(*self._args,
                                                    **self._kwargs)
        def join(self, *args):
            Thread.join(self, *args)
            return self._return

    try:
        threads = []
        participant.id=GLOBALS[0]
        for d in driver:
            participant.id += 1
            t = ThreadWithReturnValue(target = test, args = (d, participant.id, ))
            threads.append(t)
            print('Created thread: ', participant.id)
            t.start()
        fail = False
        for t in threads:
            status = t.join()
            print('Finished thread: {0} With code: {1}'.format(participant.id, status))
            if(status != 0):
                fail = True
        if(fail == True):
            raise Exception('One of the participants failed')

    except Exception as e:
        print('Exception Handled in Main, Details of the Exception:', e)
        sys.exit(-1)

def test(driver, participant_id): #test
    # room connect options
    room = 'TEST_10P_2P_Audio_MediumVideo_iceRelay'
    identity = 'Participant' + str(participant_id) + '_' + room
    realm = 'stage'
    type = 'p2p'
    audio = 'true'
    video = 'true'
    insights = 'true'
    logLevel = 'off'
    iceTransportPolicy = 'relay'

    #next participant without tracks
    if (len(GLOBALS) > 1):
        audio = 'false'
        video = 'false'

    preferredAudioCodec = 'opus-dtx'
    videoWidth = '854'
    videoHeight = '480'
    demoAppDomain = 'sdksqe-rtc-demo-app.appspot.com'
    demoAppAuth = 'https://chumba:wumba@' + demoAppDomain + '/video_v2'
    demoAppUrl = 'https://' + demoAppDomain + '/video_v2?room=' + room + '&identity=' + identity + '&realm=' + realm + '&type=' + type + '&audio=' + audio + '&video=' + video + '&insights=' + insights + \
        '&logLevel=' + logLevel + '&iceTransportPolicy=' + iceTransportPolicy + '&preferredAudioCodec=' + \
        preferredAudioCodec + '&videoWidth=' + videoWidth + '&videoHeight=' + videoHeight

    take = 10
    interval = 60
    elementTimeout = 35
    mediaElementTimeout = 60

    # open webpage
    driver.navigate_to(demoAppAuth)
    driver.navigate_to(demoAppUrl)
    driver.e('css', 'body').wait_until_visible(elementTimeout)  # 35
    driver.e('css', '#join-button').wait_until_visible(elementTimeout)  # 35

    # join room
    driver.e('css', '#join-button').click()
    time.sleep(mediaElementTimeout)  # 60s

    # check if not Disconnected
    for i in range(take):
        # page still loaded
        driver.e('css', 'body').wait_until_visible(elementTimeout)  # 35s
        # participant not disconnected
        time.sleep(interval)  # 60s
        # disconect
        time.sleep(interval)  # 60s
        driver.e('css', '#disconnect-button').wait_until_visible(elementTimeout).click()
        
    pass
    return 0

