FROM python:3.8-slim-buster

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

ADD ./backend /opt/app/
WORKDIR /opt/app

RUN python -m pip install -r requirements.txt
RUN python -m pip install gunicorn

RUN adduser --disabled-password --gecos '' worker
USER worker

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
