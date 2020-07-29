FROM debian:buster

# install packages
RUN apt update &&\
    apt install -y\
        python3.7 python3-pip

# add source
COPY . /app/
WORKDIR /app

# install python dep
RUN pip3 install discord PyNaCl

# store /data
VOLUME [ "/data" ]

# on server start
CMD python3.7 src/bot.py
