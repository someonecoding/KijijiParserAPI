FROM python:3.10.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /scraper/requirements.txt

WORKDIR /scraper

COPY ./scraper /scraper/

RUN pip3 install -r ./requirements.txt