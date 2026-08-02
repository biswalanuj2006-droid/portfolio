#!/usr/bin/env bash
# Render build script for anuj-portfolio
# Runs on every deploy: install deps, migrate, seed demo data, collect static.
set -o errexit
set -o pipefail

pip install --upgrade pip
pip install -r requirements.txt

python manage.py migrate --noinput

# Seed only when an admin password is configured, so a bare repo still deploys.
if [ -n "$ADMIN_PASSWORD" ]; then
  python manage.py seed_data
else
  echo "ADMIN_PASSWORD not set - skipping seed_data (admin sync runs on login)."
fi

python manage.py collectstatic --noinput
