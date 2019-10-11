# pull official base image
FROM python:3.7.4-alpine

# set work directory
WORKDIR /usr/src/mqtt_http_api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/mqtt_http_api/Pipfile
RUN pipenv install --skip-lock --system --dev

# copy project
COPY . /usr/src/mqtt_http_api/

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8002

CMD ["python", "app/api.py"]
