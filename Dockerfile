FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
EXPOSE 8000
WORKDIR /app

RUN apt install ca-certificates
COPY poetry.lock pyproject.toml ./
RUN pip install poetry==1.2.0 && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY ./server/ /app

CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080 main:app