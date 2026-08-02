"""Middleware that logs anonymous visitor activity for dashboard stats."""
from django.conf import settings

from .models import Visitor

_EXCLUDED_PREFIXES = ("/admin", "/admin-panel", "/static", "/media")


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class DynamicCSRFTrustMiddleware:
    """Auto-trust the current host for CSRF on hosting platforms.

    Platforms like Render and Railway assign unpredictable subdomains
    (e.g. *.onrender.com, *.up.railway.app), so instead of hard-coding
    CSRF_TRUSTED_ORIGINS we append the live origin for those domains.
    Safe for local dev (localhost is never added).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host.endswith(settings.PAAS_ALLOWED_HOST_SUFFIXES) and not settings.DEBUG:
            origin = f"https://{host}"
            if origin not in settings.CSRF_TRUSTED_ORIGINS:
                settings.CSRF_TRUSTED_ORIGINS.append(origin)
        return self.get_response(request)


class VisitorMiddleware:
    """Tracks one Visitor row per session (never breaks the request flow)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            path = request.path
            if request.method != "GET" or path.startswith(_EXCLUDED_PREFIXES):
                return response
            session = request.session
            if not session.session_key:
                session.create()
            Visitor.objects.get_or_create(
                session_key=session.session_key,
                defaults={
                    "path": path,
                    "ip": _client_ip(request),
                    "user_agent": request.META.get("HTTP_USER_AGENT", "")[:500],
                },
            )
        except Exception:
            pass  # tracking must never break the site
        return response
