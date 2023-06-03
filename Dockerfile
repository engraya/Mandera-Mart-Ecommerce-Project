FROM python:3.10.6

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ADD . /app/


COPY ./requirements.txt /app/requirements.txt


RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8000

CMD python manage.py runserver

