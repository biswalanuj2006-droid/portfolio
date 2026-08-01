"""Global template context: profile, site settings, social links, year."""
from django.utils import timezone

from .models import Profile, SiteSettings, SocialLink


def site_globals(request):
    """Provide shared data to every template (viewer and admin)."""
    try:
        profile = Profile.load()
        site = SiteSettings.load()
    except Exception:  # tables may not exist yet on very first request
        profile, site = None, None
    try:
        social_links = list(SocialLink.objects.all())
    except Exception:
        social_links = []
    return {
        "profile": profile,
        "site_settings": site,
        "social_links": social_links,
        "current_year": timezone.now().year,
    }
