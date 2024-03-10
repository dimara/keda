FROM debian:jessie

RUN rm /etc/apt/sources.list
RUN printf "deb http://archive.debian.org/debian wheezy main" > /etc/apt/sources.list.d/wheezy.list
RUN printf "deb http://archive.debian.org/debian jessie main" > /etc/apt/sources.list.d/jessie.list

RUN echo 'Acquire::Check-Valid-Until "0";' > /etc/apt/apt.conf.d/10archive

RUN apt-get update

RUN apt-get install procps nginx gunicorn -y --force-yes

RUN apt-get install python-django/wheezy python-django-south/wheezy -y --force-yes

# wget https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_amd64.deb
ADD dumb-init_1.2.5_amd64.deb /
RUN dpkg -i dumb-init_1.2.5_amd64.deb

# https://stackoverflow.com/a/41797247
RUN apt-get install locales locales-all -y --force-yes
# RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8

ADD examples/keda.gunicorn /etc/gunicorn.d/keda
ADD examples/keda.nginx /etc/nginx/sites-enabled/keda

RUN apt-get install openssl -y --force-yes
# https://stackoverflow.com/questions/10175812/how-to-generate-a-self-signed-ssl-certificate-using-openssl
RUN openssl req -x509 -newkey rsa:4096 -keyout /etc/ssl/private/keda.key -out /etc/ssl/certs/keda.pem -sha256 -days 3650 -nodes -subj "/C=GR/ST=Attica/L=Athens/O=KedaZ/OU=Reception/CN=KedaZ"

ADD . /keda

WORKDIR /keda

# https://stackoverflow.com/questions/22541333/have-nginx-access-log-and-error-log-log-to-stdout-and-stderr-of-master-process
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log
RUN ln -sf /dev/stdout /var/log/gunicorn/keda.log

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

CMD ["./start.sh"]
