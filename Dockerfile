FROM python:3.7.3-alpine3.8 as builder

ENV PIPENV_PYPI_MIRROR=https://mirrors.aliyun.com/pypi/simple/

RUN apk add --no-cache gcc musl-dev  make

RUN pip3 install pipenv --no-cache-dir
COPY Pipfile Pipfile.lock /app/

WORKDIR /app

RUN set -ex && mkdir .venv && pipenv install --deploy

FROM python:3.7.3-alpine3.8

COPY --from=builder /app /app
COPY . /app

WORKDIR /app

RUN python -m compileall .

ENV SANIC_WORKERS=1

EXPOSE 8000

CMD [".venv/bin/python3", "run.py"]