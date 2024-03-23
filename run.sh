#!/bin/sh

IMAGE=${IMAGE:-keda:latest}
DATA=${DATA:-`realpath data`}

docker run -d --name keda \
	--restart always \
	-p 8443:443 \
	-v ${DATA}:/data \
	${IMAGE}
