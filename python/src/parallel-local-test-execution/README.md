# Py-TestUI test scripts

## Prerequisites

- Change active directory to `scripts/python` and follow instructions

- Install chromedriver (check if installed with `chromedriver -v`)

  ```
  brew install chromedriver geckodriver
  ```

- Install Python

  ```
  brew install python
  ```

- Create virtual environment

  ```
  python3 -m venv venv
  ```

- Activate virtual enviornment

  ```
  source venv/bin/activate
  ```

- Install depenendencies

  ```bash
  pip3 install -r requirements.txt
  ```

- When done modifying virtual environment, leave it
  ```
  deactivate
  ```

## Run tests

- Use the following to execute your tests:

  ```
  ./venv/bin/pytest ./src/{FILE_NAME}.py -s -m loaderotest
  ```

- Use the following to execute your tests (venv is already activated):

  ```
  pytest -s ./src/{FILE_NAME}.py -m loaderotest
  ```

- Use the following to execute your tests with parametars (venv is already activated):

  ```
  export NUMBER_OF_PARTICIPANTS={NUMBER_OF_PARTICIPANTS}
  export SELENIUM_REMOTE_URL={SELENIUM_REMOTE_URL}
  pytest -s ./src/{FILENAME}.py -m loaderotest
  ```

## Docker

- Build image from Dockerfile

  ```
  docker build -t {IMAGE_NAME} .
  ```

- Run image from Dockerfile 

  ```
  docker run -it {IMAGE_NAME}
  ```

- Run image from Dockerfile with parametars

  ```
  docker run -it -e NUMBER_OF_PARTICIPANTS='{NUMBER_OF_PARTICIPANTS}' -e SELENIUM_REMOTE_URL='{SELENIUM_REMOTE_URL}' {IMAGE_NAME}
  ```
