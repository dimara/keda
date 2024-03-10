## Install

1. Clone the repo:
   ```
   git clone https://github.com/dimara/keda
   ```

1. Create the Docker image:
   ```
   docker build -t keda:latest .
   ```

1. Create a self-signed SSL certificate:
   ```
   openssl req -x509 -newkey rsa:4096 \
     -keyout keda.key \
     -out keda.pem \
     -sha256 -days 3650 -nodes \
     -subj "/C=GR/ST=Attica/L=Athens/O=KedaZ/OU=Reception/CN=KedaZ"
   ```

1. Start the container:
   ```
   docker run -d --name keda \
         -p 8443:443 \
         -v $PWD/keda.key:/etc/ssl/private/keda.key \
         -v $PWD/keda.pem:/etc/ssl/certs/keda.pem \
         -v $PWD/db.sqlite3:/keda/db.sqlite3 \
         keda:latest
   ```

1. Create super user:
   ```
   docker exec -ti keda \
          python manage.py createsuperuser \
              --username admin --email=admin@example.com
   ```

1. Open your browser and visit https://127.0.0.1:8443/.
