VERSION := $(shell git describe --first-parent --tags --dirty)
GIT_ROOT := $(shell git rev-parse --show-toplevel)

IMAGE_REPO := keda
IMAGE_TAG ?= $(VERSION)
IMAGE ?= $(IMAGE_REPO):$(IMAGE_TAG)

docker-build:
	docker build -t $(IMAGE) -f Dockerfile .

# Start a tmp container for preview
docker-run:
	docker run --rm --name keda \
		-p 8443:443 \
		-v $(GIT_ROOT)/data:/data \
		$(IMAGE)
