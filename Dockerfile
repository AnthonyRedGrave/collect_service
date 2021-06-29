FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY collect_service/ /code/

COPY init.sql /docker-entrypoint-initdb.d/
# RUN python manage.py makemigrations

# RUN python manage.py migrate