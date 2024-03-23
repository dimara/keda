## Install

1. Install Docker by following [official docs](https://docs.docker.com/engine/install/debian/)

1. Clone the repo:
   ```
   git clone https://github.com/dimara/keda
   ```

1. Specify the docker image:
   ```
   export IMAGE=keda:latest
   ```

1. Create the Docker image:
   ```
   make docker-build
   ```

1. Place your SSL certificate under ``data/keda.key`` and ``data/keda.pem``.
   If you skip this step the image will create a self-signed on upon startup.

1. Start the container:
   ```
   docker run -d --name keda \
      --restart always \
      -p 8443:443 \
      -v $PWD/data:/data \
      ${IMAGE?}
   ```

1. Create super user:
   ```
   docker exec -ti keda \
          python manage.py createsuperuser \
              --username admin --email=admin@example.com
   ```

1. Open your browser and visit https://127.0.0.1:8443/.
