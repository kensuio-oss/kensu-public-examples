FROM python:3.8-slim-buster

RUN mkdir /app
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt  
RUN pip install kensu-1.7.2.0.tar.gz 

WORKDIR /app/python_code

ENTRYPOINT ["/bin/bash", "-c"]