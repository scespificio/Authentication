#!/bin/sh
set -e

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

echo "🏁 Démarrage du backend Django…"

echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

echo "👉 Application des migrations"
python manage.py migrate --noinput || echo "[WARN] migrate failed"

echo "👉 Lancement de Gunicorn"
exec gunicorn config.wsgi:application -b 0.0.0.0:900 -w 4
