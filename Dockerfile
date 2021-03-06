FROM python:3.4

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        mysql-client \
        nginx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/ask_ermishechkin
COPY app/requirements.txt ./
RUN pip install -r requirements.txt
COPY nginx.conf /etc/nginx/
COPY django /etc/gunicorn.d/
COPY app .
CMD bash -c "service nginx restart && gunicorn -b 0.0.0.0:8000 ask_ermishechkin.wsgi"
