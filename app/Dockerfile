FROM python:3.7-alpine

RUN mkdir /application
RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev

## set environment variables for security concern
ENV PYTHONDONTWRITEBYTECODE="true" \
    PYTHONUNBUFFERED="true"

WORKDIR /application

COPY requirements.txt /application

RUN pip3 install -r requirements.txt

COPY . /application

CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "wsgi"]
