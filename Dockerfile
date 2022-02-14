FROM python:3.8-slim-buster

RUN mkdir /app
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt  

WORKDIR /app/python_code

ENTRYPOINT ["/bin/bash", "-c"]