#!/usr/bin/env bash
# Render build script for anuj-portfolio
# Runs on every deploy: install deps, migrate, seed demo data, collect static.
set -o errexit
set -o pipefail

pip install --upgrade pip
pip install -r requirements.txt

# Migrate with retries: the free Postgres instance may still be provisioning
# on the very first Blueprint deploy, so don't fail the build instantly.
for attempt in 1 2 3 4 5; do
  if python manage.py migrate --noinput; then
    break
  fi
  echo "migrate failed (attempt $attempt/5) - retrying in 10s..."
  sleep 10
done

# Seed only when an admin password is configured, so a bare repo still deploys.
if [ -n "$ADMIN_PASSWORD" ]; then
  python manage.py seed_data
else
  echo "ADMIN_PASSWORD not set - skipping seed_data (admin sync runs on login)."
fi

python manage.py collectstatic --noinput
