FROM python:3.8-slim-buster

# Install OpenJDK-11
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;


RUN mkdir /app
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt  

WORKDIR /app/python_code

ENTRYPOINT ["/bin/bash", "-c"]