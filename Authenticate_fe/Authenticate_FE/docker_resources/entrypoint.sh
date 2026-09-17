#!/bin/sh
set -e

# Valeurs par défaut possibles si non fournies par docker-compose
: "${VITE_BACKEND_URL:=http://localhost:900}"
: "${VITE_BACKEND_TIMEOUT:=5000}"
: "${ALLOWED_HOST:=localhost,127.0.0.1}"

cat <<EOF >/usr/share/nginx/html/config.js
window.__APP_CONFIG__ = {
  BACKEND_URL: "${VITE_BACKEND_URL}",
  BACKEND_TIMEOUT: ${VITE_BACKEND_TIMEOUT},
  ALLOWED_HOST: "${ALLOWED_HOST}"
};
EOF

# On lance Nginx
exec nginx -g "daemon off;"
