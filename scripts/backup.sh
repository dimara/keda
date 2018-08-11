#!/bin/bash

set -e

LOGFILE=/var/log/keda-backup.log
DB=/root/keda/db.sqlite3
BACKUPDIR=/backup

# NOTE: This will send email notifications
exec &> >(tee -a $LOGFILE)
#exec 1>> $LOGFILE 2>&1


function log() {

        echo -e "$(date) keda-backup $@" >&2

}

function timestamp() {
        date -u +%Y%m%d%H%M%S
}


log Starting backup...

if [ ! -f $DB ]; then
	log Database $DB not found. Aborting.
	exit 1
fi

if [ ! -d $BACKUPDIR ]; then
	log Backup dir $BACKUPDIR not found. Aborting.
	exit 1
fi

log Cleaning backups older than 30 days...
find ${BACKUPDIR}/ -maxdepth 1 -type f -name 'db.sqlite3.*' -mtime +30 -print0 | xargs -r -0 -n1 rm -v

log Stopping gunicorn...
service gunicorn stop

log Syncing fileystems...
sync

backup=${BACKUPDIR}/db.sqlite3.$(timestamp)
log Copying database $DB.to $backup..
cp -av $DB $backup

log Starting gunicorn...
service gunicorn start

log Backup finished successfully.
