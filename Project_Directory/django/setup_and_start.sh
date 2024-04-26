#!/bin/sh

database_inaccessible() {
  export PGPASSWORD=$POSTGRES_PASSWORD
  psql --host=postgres \
    --username=$POSTGRES_USER \
    --dbname=$POSTGRES_DB \
    --command="\dt"
  [ $? -ne 0 ]
  return $?
}

while database_inaccessible ; do
  echo "Waiting for database"
  sleep 2
done

echo "Copying static resources to STATIC_ROOT"
python3 manage.py collectstatic --noinput

echo "Starting uwsgi Django server"
exec uwsgi --socket /var/www/uwsgi/uwsgi.sock \
  --chmod-socket=666 \
  --workers 4 \
  --buffer-size=32768 \
  --wsgi-file /usr/src/django/djangoproject/djangoproject/wsgi.py
