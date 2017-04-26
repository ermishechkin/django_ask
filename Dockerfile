FROM python:3.4

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        mysql-client \
        nginx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/ask_ermishechkin
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY app .

