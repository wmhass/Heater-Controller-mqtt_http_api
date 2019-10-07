FROM python:3.7

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/mqtt_http_api
WORKDIR /usr/src/mqtt_http_api

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/mqtt_http_api/Pipfile
RUN pipenv install --skip-lock --system --dev

COPY . /usr/src/mqtt_http_api/

EXPOSE 8888

CMD ["python", "app/api.py"]
