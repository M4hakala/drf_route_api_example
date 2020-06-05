FROM python:3.7

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED 1

RUN mkdir /config
ADD requirements.txt /config
RUN pip install -r /config/requirements.txt

RUN mkdir /app
WORKDIR /app
