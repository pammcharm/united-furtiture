#!/usr/bin/env bash
set -o errexit

python -m pip install -r requirements.txt
npm ci
npm run build
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_united_furniture
python manage.py create_default_admin
