"""Custom template tags and filters."""
from django import template

register = template.Library()


@register.filter
def get_attr(obj, name):
    """Return obj.<name> or None (safe dynamic attribute access)."""
    return getattr(obj, name, None)


@register.simple_tag
def active_class(request, url_name):
    """Return 'active' when the current page matches the given url name."""
    if request and request.resolver_match and request.resolver_match.url_name == url_name:
        return "active"
    return ""


@register.filter
def file_size_label(value):
    """Human friendly file size for uploaded files."""
    try:
        size = value.size
    except (AttributeError, ValueError, OSError):
        return ""
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024
    return ""
