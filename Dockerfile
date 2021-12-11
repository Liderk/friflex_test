FROM python:3.8-alpine
LABEL author='vismoke@gmail.com' version=1.0 project='course_api'
WORKDIR /code
COPY requirements.txt .
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libffi-dev \
                  && pip install --upgrade pip \
                  && pip install -r requirements.txt \
                  && rm -rf .cache/pip
COPY . /code
RUN export SECRET_KEY=test_SECRET_KEY && python manage.py collectstatic --noinput