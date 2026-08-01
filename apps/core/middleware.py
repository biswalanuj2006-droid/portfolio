"""Middleware that logs anonymous visitor activity for dashboard stats."""
from .models import Visitor

_EXCLUDED_PREFIXES = ("/admin", "/admin-panel", "/static", "/media")


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


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
