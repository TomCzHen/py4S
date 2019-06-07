ARG python_version="3.7.3"
ARG alpine_version="3.9"
ARG pypi_mirror="https://mirrors.aliyun.com/pypi/simple/"

FROM python:${python_version}-alpine${alpine_version} as builder

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install -U pip --no-cache-dir \
    && pip install pipenv --no-cache-dir

ENV PIPENV_PYPI_MIRROR=${pypi_mirror} PYTHONDONTWRITEBYTECODE=1

COPY Pipfile Pipfile.lock /app/

WORKDIR /app

RUN mkdir .venv && pipenv install --deploy

FROM python:${python_version}-alpine${alpine_version}

COPY --from=builder /app /app
COPY . /app

WORKDIR /app

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    SANIC_WORKERS=1

EXPOSE 8000

CMD ["python", "run.py"]