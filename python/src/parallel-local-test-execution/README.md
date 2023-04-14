# Parallel local test execution

## Prerequisites

- Note: The following set up refers to Mac OS.

- Change active directory to `python/src/parallel-local-test-execution` and follow the instructions

- Install chromedriver (check if installed with `chromedriver -v`)

  ```
  brew install chromedriver geckodriver
  ```

- Install Python (v3.9.10 used)

  ```
  brew install python
  ```

- Create virtual environment

  ```
  python -m venv venv
  ```

- Activate virtual enviornment

  ```
  source venv/bin/activate
  ```

- Install depenendencies

  ```bash
  pip install -r requirements.txt
  ```

- When done modifying virtual environment, leave it
  ```
  deactivate
  ```

## Run tests

- Use the following command to execute your test:

  ```
  ./venv/bin/pytest ./src/test_on_loadero.py -s -m demotest
  ```

- Use the following command to execute your test (venv is already activated):

  ```
  pytest -s ./src/test_on_loadero.py -m demotest
  ```

- Use the following command to execute your test with parameters (venv is already activated):

  ```
  export NUMBER_OF_PARTICIPANTS={NUMBER_OF_PARTICIPANTS}
  export SELENIUM_REMOTE_URL={SELENIUM_REMOTE_URL}
  pytest -s ./src/{FILENAME}.py -m loaderotest
  ```

## Test scenario
- NUMBER_OF_PARTICIPANTS participants navigate to https://janus.conf.meetecho.com/videoroomtest.html
- NUMBER_OF_PARTICIPANTS participants join the room
- NUMBER_OF_PARTICIPANTS participants stay in the room for 2 minutes
- NUMBER_OF_PARTICIPANTS participants leave the room
