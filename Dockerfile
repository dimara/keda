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
  python3-django

# https://stackoverflow.com/a/41797247
RUN apt install locales locales-all -y
# RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8

ADD examples/keda.nginx /etc/nginx/sites-enabled/keda
RUN rm -f /etc/nginx/sites-enabled/default

ADD . /keda

WORKDIR /keda

# https://stackoverflow.com/questions/22541333/have-nginx-access-log-and-error-log-log-to-stdout-and-stderr-of-master-process
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

CMD ["./start.sh"]
