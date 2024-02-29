# syntax=docker/dockerfile:1

# Installing Python
FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y git

WORKDIR /application

COPY requirements.txt /application

RUN python -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

# Tools for debug
RUN apt-get install iputils-ping -y

COPY . /application/

RUN ls -la

EXPOSE 8000
