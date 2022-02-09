FROM tensorflow/tensorflow@sha256:fc5eb0604722c7bef7b499bb007b3050c4beec5859c2e0d4409d2cca5c14d442

RUN \
  apt-get update && \
  export DEBIAN_FRONTEND=noninteractive && \
  apt-get install -y \
    ffmpeg \
    libcairo2-dev \
    cmake && \
  apt-get autoremove -y && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN \
  pip install --upgrade pip && \
  pip install --upgrade setuptools && \
  pip install -r requirements.txt
