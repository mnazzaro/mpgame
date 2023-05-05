# syntax=docker/dockerfile:1

FROM python:3.9-buster

RUN apt-get update
RUN python -m pip install --upgrade pip


########## Install mplib ###########

WORKDIR /lib

RUN git clone https://github.com/mnazzaro/mplib
WORKDIR /lib/mplib
RUN git checkout new-auth
RUN python -m pip install .

########## Install mpgame ###########

WORKDIR /source

# Install dependencies
RUN python -m pip install flask Flask-SocketIO flask_CORS celery
RUN python -m pip install gunicorn==20.1.0
RUN python -m pip install eventlet==0.30.2

RUN git clone https://github.com/mnazzaro/mpgame
WORKDIR /source/mpgame
RUN python -m pip install .

########## Start Gunicorn ##########

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "-k", "eventlet", "-w", "1", "entry_point:sio"]

