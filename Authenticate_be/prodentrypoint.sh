#!/bin/sh
set -e

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

echo "🏁 Démarrage du backend Django…"

echo "👉 Collecte des statiques"
python manage.py collectstatic --noinput || echo "[WARN] collectstatic failed (c’est peut-être normal)"

echo "👉 Application des migrations"
python manage.py migrate --noinput || echo "[WARN] migrate failed"

echo "👉 Lancement de Gunicorn"
exec gunicorn Authenticate.wsgi:application -b 0.0.0.0:5180 -w 4
