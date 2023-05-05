# syntax=docker/dockerfile:1

FROM python:3.9-buster

RUN apt-get update & apt-get install git
RUN python -m pip install --upgrade pip


########## Install mplib ###########

WORKDIR /lib

ENV MPLIB_COMMIT=b908987a6bbecfd914cfedb1122b22cf74828a0f

RUN rm -rf /lib/mplib
RUN git clone https://github.com/mnazzaro/mplib
WORKDIR /lib/mplib
RUN git reset --hard $MPLIB_COMMIT
RUN python -m pip install -e .

########## Install mpgame ###########

WORKDIR /source

# Install dependencies
RUN python -m pip install gunicorn==20.1.0
RUN python -m pip install eventlet==0.30.2
RUN python -m pip install psycopg2


ENV MPGAME_COMMIT=718273e57756228dfaeb960bbbc5815f13e8a7b9

RUN rm -rf /source/mpgame
RUN git clone https://github.com/mnazzaro/mpgame
WORKDIR /source/mpgame
RUN git reset --hard $MPGAME_COMMIT
RUN python setup.py install

########## Start Gunicorn ##########

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "-k", "eventlet", "-w", "1", "entry_point:app"]

