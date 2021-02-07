FROM python:3.8

ENV PYTHONUNBUFFERED=1


RUN mkdir /fastapi-auth
COPY . /fastapi-auth
WORKDIR /fastapi-auth

RUN pip install --upgrade pip
RUN pip install -r requirements.txt