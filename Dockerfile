# With bookworm apt update fails with NO_PUBKEY
# https://serverfault.com/questions/1137215/how-can-i-write-a-dockerfile-based-on-debian-slim-in-which-apt-get-update-does
#FROM debian:bookworm-20240311
FROM debian:bullseye-20240311

RUN apt update && apt install -y \
  procps \
  nginx \
  gunicorn \
  dumb-init \
  openssl \
  python3-django \
  python3-reportlab \
  fonts-dejavu

# https://stackoverflow.com/a/41797247
RUN apt install locales locales-all -y
# RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8

RUN apt install python3-pip --no-install-recommends -y

# XXX: This will bring python-monkey-business
# https://github.com/pypa/pip/issues/11717#issuecomment-1378384449
#RUN pip3 install django-nested-admin==4.0.2
ADD wheels /tmp/wheels
RUN pip3 install --no-index --find-links /tmp/wheels django-nested-admin==4.0.2 django-dbbackup==4.1.0

ADD sqlite.py /usr/local/lib/python3.9/dist-packages/dbbackup/db/sqlite.py

RUN apt install vim sqlite3 gnuplot-nox --no-install-recommends -y

ADD examples/keda.nginx /etc/nginx/sites-enabled/keda
RUN rm -f /etc/nginx/sites-enabled/default

# https://gist.github.com/mowings/59790ae930accef486bfb9a417e9d446
RUN apt install rsyslog cron -y
RUN sed -i '/imklog/s/^/#/' /etc/rsyslog.conf
RUN sed -i '/imudp/s/^#//' /etc/rsyslog.conf
ADD examples/keda.rsyslog /etc/rsyslog.d/keda.conf
ADD examples/keda.cron /etc/cron.d/keda

ADD . /keda

WORKDIR /keda

# https://stackoverflow.com/questions/22541333/have-nginx-access-log-and-error-log-log-to-stdout-and-stderr-of-master-process
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

CMD ["./start.sh"]
