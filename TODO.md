### Pre-built docker image

Create a docker image with everything pre-installed and allow the user to start
a container and optionally override the sqlite database or/and the code using
bind mounts. The image should run systemd with gunicorn and NGINX services
enabled.

### Upgrade to Debian buster and Django 1.11

Currenlty this works on Debian jessie and Django 1.4. We need to support
Debian buster and Djano 1.11 and be able to upgrade existing deployments
seamlessly.

### Upgrade to Python3

Switch to Python3 so that we can upgrade to Debian bullseye and Django 2.2

### Compare with related platforms

Compare with protel, fidelio software, and opera.

### Reservations

In reservation page add a footer showing stats for confirmed, etc.

### Receipts

Suuport printing receipts based on the reservation.

### Extra tags

Tag persons that are about to leave today.

### Mail notifications

Configure mail notifications for daily backup, failures, etc.
