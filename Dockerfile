FROM python:3.9-slim-buster

ADD ./backend /opt/app/
WORKDIR /opt/app

RUN python setup.py install
RUN python -m pip install gunicorn

RUN adduser --disabled-password --gecos '' worker
USER worker

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
