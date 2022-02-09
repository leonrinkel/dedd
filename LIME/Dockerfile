FROM ubuntu:18.04

RUN \
    apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        zlib1g-dev \
        libjpeg-dev

WORKDIR /app

COPY requirements.txt .
RUN \
    pip3 install --upgrade pip && \
    pip3 install --upgrade setuptools && \
    pip3 install -r requirements.txt

COPY . .
