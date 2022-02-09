FROM ubuntu:16.04

RUN \
  apt-get update && \
  export DEBIAN_FRONTEND=noninteractive && \
  apt-get install -y \
    python \
    python-pip \
    cmake \
    python-opencv && \
  apt-get autoremove -y && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN \
  pip install --upgrade pip==20.3.4 && \
  pip install --upgrade setuptools==44.1.1 && \
  pip install -r requirements.txt
