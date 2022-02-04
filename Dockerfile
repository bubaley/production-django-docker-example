FROM python:3.9.2-alpine3.13
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code

RUN apk update && apk add gcc python3-dev musl-dev libffi-dev gettext
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -U pip setuptools
RUN pip install -r requirements.txt
COPY . /code/