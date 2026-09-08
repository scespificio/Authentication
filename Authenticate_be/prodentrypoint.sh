#!/bin/sh
set -e

if [ "$#" -gt 0 ]; then
  exec "$@"
fi
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear


echo "👉 Lancement de Gunicorn"
exec gunicorn Authenticate.wsgi:application -b 0.0.0.0:900 -w 4
