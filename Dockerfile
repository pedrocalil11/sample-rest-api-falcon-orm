FROM python:3.9-alpine
ARG PROJECT_NAME=sample_api
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip3 install psycopg2 \
  && apk del build-deps
COPY requirements.txt /requirements.txt
COPY rds-ca-2019-root.pem /rds-ca-2019-root.pem
RUN pip3 install -r /requirements.txt
COPY src /app
WORKDIR /app

EXPOSE 3000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "app:api", "--timeout", "102"]