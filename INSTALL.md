## Local install using Docker

1. Clone the repo:
   ```
   git clone https://github.com/dimara/keda
   ```

1. Start a wheezy container:

   ```
   docker run -d -ti \
     -p 8000:8000 \
     -p 443:443 \
     --name keda \
     -v $PWD/keda:/keda \
     -v /backup:/backup \
     -w /keda \
     -e LANG=en_US.UTF-8 \
     debian:wheezy
   ```

1. Exec into the container:
   ```
   docker exec -ti keda bash
   ```

1. Enable wheezy APT repo from archives (see also https://wiki.debian.org/DebianWheezy):
   ```
   cat <<EOF > /etc/apt/sources.list/wheezy.list
   deb http://archive.debian.org/debian wheezy main
   deb http://archive.debian.org/debian-security wheezy/updates main
   EOF
   ```
   ```
   cat <<EOF > /etc/apt/apt.conf.d/10archive
   Acquire::Check-Valid-Until "0";
   EOF
   ```


1. Install deps:
   ```
   apt-get update
   apt-get install procps nginx gunicorn python-django/wheezy python-django-south/wheezy gnuplot -y
   ```

1. Configure locales:
   ```
   apt-get install -y locales
   echo en_US.UTF-8 UTF-8 >> /etc/locale.gen
   locale-gen
   ```

1. Initialize the Django app:
   ```
   python manage.py syncdb --noinput
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser --username=admin --email=admin@example.com
   ```

1. Start the server:
   ```
   python manage.py runserver 0.0.0.0:8000
   ```

1. Open your browser and visit http://127.0.0.1:8000.


### NGINX + gunicorn

1. Configure gunicorn:
   ```
   cp examples/keda.gunicorn /etc/gunicorn.d/keda
   ```

1. Configure NGINX:
   ```
   cp examples/keda.nginx /etc/nginx/sites-enabled/keda
   ```

1. Create SSL cert:
   ```
   openssl req -new -x509 -days 365000 -nodes -out /etc/ssl/certs/keda.pem -keyout /etc/ssl/private/keda.key
   ```

1. Start gunicorn:
   ```
   service gunicorn restart
   ```

1. Start NGINX:
   ```
   service nginx restart
   ```
1. Open your browser and visit https://127.0.0.1.
