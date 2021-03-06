# syntax = docker/dockerfile:experimental
FROM debian:buster

# install packages
RUN apt update &&\
    apt install -y\
        python3.7 python3-pip\
        ffmpeg

# add source
COPY . /app/
WORKDIR /app

# install python dep
RUN pip3 install discord PyNaCl

# store /data
VOLUME [ "/app/data" ]

# on server start
CMD python3.7 src/bot.py
