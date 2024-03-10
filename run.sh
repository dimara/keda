#!/bin/sh

docker run -d --name keda \
	--restart always \
	-p 8443:443 \
	-v $PWD/keda.key:/etc/ssl/private/keda.key \
	-v $PWD/keda.pem:/etc/ssl/certs/keda.pem \
	-v $PWD/db.sqlite3:/keda/db.sqlite3 \
	keda:latest
