FROM python:3

WORKDIR /loadero_local_setup

ADD pytest.ini ./

ADD requirements.txt ./

COPY ./src ./src

RUN pip install virtualenv

RUN python -m venv venv

RUN . venv/bin/activate

RUN pip install -r requirements.txt

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD [ "pytest", "-s", "./src/test_on_loadero.py", "-m", "loaderotest" ]
