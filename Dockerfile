# syntax=docker/dockerfile:1

FROM python:3.9-buster

RUN apt-get update & apt-get install git
RUN python -m pip install --upgrade pip


########## Install mplib ###########

WORKDIR /lib

RUN rm -rf /lib/mplib
RUN git clone https://github.com/mnazzaro/mplib
WORKDIR /lib/mplib
RUN git checkout develop
RUN python -m pip install -e .

########## Install mpgame ###########

WORKDIR /source

# Install dependencies
RUN python -m pip install gunicorn==20.1.0
RUN python -m pip install eventlet==0.30.2
RUN python -m pip install psycopg2


RUN rm -rf /source/mpgame
RUN git clone https://github.com/mnazzaro/mpgame
WORKDIR /source/mpgame
RUN git checkout develop
RUN python setup.py install

########## Start Gunicorn ##########

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "eventlet",  "-w", "2", "entry_point:app"]

