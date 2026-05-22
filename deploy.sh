#!/bin/bash
set -e

echo "--- Deploy: $(date) ---"

cd /home/Aurineque/escala-app

echo "Puxando codigo..."
git pull origin main

echo "Aplicando migracoes..."
python manage.py migrate --noinput

echo "Coletando estaticos..."
python manage.py collectstatic --noinput

echo "Recarregando aplicacao..."
curl -s -X POST "https://www.pythonanywhere.com/api/v0/user/Aurineque/webapps/Aurineque.pythonanywhere.com/reload/" \
    -H "Authorization: Token $PA_API_TOKEN"

echo "--- Deploy concluido ---"
