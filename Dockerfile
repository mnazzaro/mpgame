# syntax=docker/dockerfile:1

FROM python:3.9-buster

RUN apt-get update
RUN python -m pip install --upgrade pip


########## Install mplib ###########

WORKDIR /lib

RUN rm -rf /lib/mplib
RUN git clone https://github.com/mnazzaro/mplib
WORKDIR /lib/mplib
RUN git checkout new-auth
RUN python setup.py install

########## Install mpgame ###########

WORKDIR /source

# Install dependencies
RUN python -m pip install gunicorn==20.1.0
RUN python -m pip install eventlet==0.30.2

ENV MPGAME_COMMIT=f3a481d4a64af3f32a7eff88ecdbb381530ceb86

RUN rm -rf /source/mpgame
RUN git clone https://github.com/mnazzaro/mpgame
WORKDIR /source/mpgame
RUN git reset --hard $MPGAME_COMMIT
RUN python setup.py install

########## Start Gunicorn ##########

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "-k", "eventlet", "-w", "1", "entry_point:sio"]

