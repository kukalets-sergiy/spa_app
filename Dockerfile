FROM python:3.10.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y iputils-ping
WORKDIR /code
# Install gettext tools
RUN apt-get update && apt-get install -y gettext
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD sh -c "python manage.py runserver 0.0.0.0:8000 & rm -f /tmp/celerybeat.pid && celery -A spa_app beat -l info"