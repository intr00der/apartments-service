FROM python:3.8.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /apart_service
WORKDIR /apart_service
COPY requirements.txt /apart_service/
RUN python3 -m pip install --upgrade pip
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev
RUN pip3 install -r requirements.txt
COPY . /apart_service/