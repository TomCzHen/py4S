FROM python:3.7.2

RUN pip3 install pipenv --no-cache-dir

RUN set -ex && mkdir /app
WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN set -ex && pipenv install --deploy --system

COPY . /app
EXPOSE 8000
CMD ["python3", "run.py"]