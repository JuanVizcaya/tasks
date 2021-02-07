FROM python:3.8.5

ENV PYTHONBUFFERED 1
RUN mkdir /code

WORKDIR /code
COPY . /code/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt
