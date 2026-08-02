"""Admin sync - guarantees a working admin login on the deployed site.

When the admin login page is opened, this reads the ADMIN_USERNAME /
ADMIN_PASSWORD / ADMIN_EMAIL environment variables and makes sure a
superuser with those credentials exists in the database. A fresh deploy
therefore always has a known admin login, even on a brand-new database.

The password is NEVER hard-coded here - set ADMIN_PASSWORD on the host
(Render dashboard -> Environment). If ADMIN_PASSWORD is missing, the sync
is skipped entirely and the login page works as before.

NOTE: While this hook is enabled, the admin password is kept in sync with
ADMIN_PASSWORD on every login, so a password changed inside the admin panel
is reverted the next time the login page is opened. To change the password,
update ADMIN_PASSWORD in the environment instead.
"""

import os

from django.contrib.auth import get_user_model


def sync_admin_user() -> bool:
    """Create/refresh the admin superuser from env vars. Returns True if changed."""
    username = os.environ.get("ADMIN_USERNAME", "Anuj-2006").strip()
    password = os.environ.get("ADMIN_PASSWORD", "")
    email = os.environ.get("ADMIN_EMAIL", "biswalanuj2006@gmail.com")

    # Never sync with a password we do not know - the environment must supply it.
    if not username or not password:
        return False

    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email, "is_staff": True, "is_superuser": True},
    )

    if created or not user.check_password(password):
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(update_fields=["email", "is_staff", "is_superuser", "password"])
        return True
    return False
