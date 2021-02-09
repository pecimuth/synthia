FROM python:3.8
WORKDIR /app
COPY . .
ENV FLASK_ENV=development
ENV FLASK_APP=web
EXPOSE 5000
RUN python -m pip install -e .
CMD python -m flask run --host=0.0.0.0 --port=5000
