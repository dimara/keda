#!/bin/sh

if [ ! -f /data/keda.key ]; then
	echo WARN: Private key for KedaZ SSL certificate not found.
	echo Generating a self-signed SSL certificate..
	# https://stackoverflow.com/questions/10175812/how-to-generate-a-self-signed-ssl-certificate-using-openssl
	openssl req -x509 -newkey rsa:4096 \
		-keyout /data/keda.key \
		-out /data/keda.pem \
		-sha256 \
		-days 3650 \
		-nodes \
		-subj "/C=GR/ST=Attica/L=Athens/O=KedaZ/OU=Reception/CN=KedaZ"
fi

echo Using SSL cert..
openssl x509 -in /data/keda.pem -text

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
