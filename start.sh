#!/bin/sh

echo Initializing/Updating Django project...
python manage.py syncdb --noinput
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py loaddata reception/fixtures/*
#python manage.py createsuperuser --username=admin --email=admin@example.com --noinput
echo Starting gunicorn...
/usr/sbin/gunicorn-debian start
echo Starting nginx...
nginx
echo Sleeping forever...
sleep infinity
