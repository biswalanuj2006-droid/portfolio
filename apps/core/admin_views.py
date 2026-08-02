"""Admin panel: dashboard, profile/settings managers and generic CRUD."""
import json
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.models.fields.files import FieldFile, ImageFieldFile
from django.db.models.functions import TruncDate
from django.db.utils import OperationalError, ProgrammingError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import (
    AchievementForm, CertificateForm, EducationForm, ExperienceForm, FAQForm,
    GalleryImageForm, ProfileForm, ProjectForm, ResumeForm, SiteSettingsForm,
    SkillForm, SocialLinkForm,
)
from .models import (
    Achievement, Certificate, ContactMessage, Education, Experience, FAQ,
    GalleryImage, Profile, Project, Resume, SiteSettings, Skill, SocialLink, Visitor,
)
from .startup import sync_admin_user

# ---------------------------------------------------------------------------
# Resource registry - single config driving the whole CRUD system (DRY)
# ---------------------------------------------------------------------------
RESOURCES = {
    "skills": {
        "model": Skill, "form": SkillForm, "title": "Skills",
        "icon": "bi-lightning-charge-fill", "fields": ["name", "category", "level", "order"],
        "search": "name", "ordering": ("category", "order", "name"),
    },
    "projects": {
        "model": Project, "form": ProjectForm, "title": "Projects",
        "icon": "bi-kanban-fill", "fields": ["title", "category", "status", "featured", "updated_at"],
        "search": "title", "ordering": ("-featured", "order", "-created_at"),
    },
    "certificates": {
        "model": Certificate, "form": CertificateForm, "title": "Certificates",
        "icon": "bi-award-fill", "fields": ["title", "issuer", "category", "issued_date"],
        "search": "title", "ordering": ("-issued_date",),
    },
    "achievements": {
        "model": Achievement, "form": AchievementForm, "title": "Achievements",
        "icon": "bi-trophy-fill", "fields": ["title", "category", "date"],
        "search": "title", "ordering": ("-date",),
    },
    "gallery": {
        "model": GalleryImage, "form": GalleryImageForm, "title": "Gallery",
        "icon": "bi-images", "fields": ["title", "category", "image", "created_at"],
        "search": "title", "ordering": ("-created_at",),
    },
    "resumes": {
        "model": Resume, "form": ResumeForm, "title": "Resumes",
        "icon": "bi-file-earmark-pdf-fill", "fields": ["label", "file", "is_active", "created_at"],
        "ordering": ("-created_at",),
    },
    "experience": {
        "model": Experience, "form": ExperienceForm, "title": "Experience",
        "icon": "bi-briefcase-fill", "fields": ["role", "company", "current", "order"],
        "search": "role", "ordering": ("order", "-start_date"),
    },
    "education": {
        "model": Education, "form": EducationForm, "title": "Education",
        "icon": "bi-mortarboard-fill", "fields": ["degree", "institution", "start_year", "end_year"],
        "search": "institution", "ordering": ("order", "-start_year"),
    },
    "social_links": {
        "model": SocialLink, "form": SocialLinkForm, "title": "Social Links",
        "icon": "bi-share-fill", "fields": ["platform", "url", "order"],
        "search": "platform", "ordering": ("order", "platform"),
    },
    "faqs": {
        "model": FAQ, "form": FAQForm, "title": "FAQ (AI Assistant)",
        "icon": "bi-robot", "fields": ["question", "order"],
        "search": "question", "ordering": ("order", "id"),
    },
}


admin_required = login_required(login_url="core:admin_login")


def _display_value(obj, field):
    """Resolve a field to (kind, value) for the generic list template."""
    getter = getattr(obj, f"get_{field}_display", None)
    raw = getter() if getter else getattr(obj, field, None)
    if isinstance(raw, ImageFieldFile) and raw:
        return "image", raw.url
    if isinstance(raw, FieldFile) and raw:
        return "file", raw.url
    if isinstance(raw, bool):
        return "bool", raw
    if raw is None:
        return "text", ""
    if hasattr(raw, "strftime"):
        return "date", raw.strftime("%d %b %Y")
    return "text", raw


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
def admin_login(request):
    """Custom glassmorphism login for the admin panel."""
    # Keep the admin account from the environment in sync on first use, so a
    # fresh deploy always has a working login (see apps/core/startup.py).
    try:
        sync_admin_user()
    except (OperationalError, ProgrammingError):
        # Database not migrated yet - the login page must still render.
        pass
    if request.user.is_authenticated:
        return redirect("core:dashboard")
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("core:dashboard")
        error = "Invalid credentials. Please try again."
    return render(request, "admin/login.html", {"error": error})


def admin_logout(request):
    logout(request)
    return redirect("core:admin_login")


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@admin_required
def dashboard(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    stats = {
        "projects": Project.objects.count(),
        "certificates": Certificate.objects.count(),
        "skills": Skill.objects.count(),
        "messages": ContactMessage.objects.count(),
        "unread_messages": ContactMessage.objects.filter(is_read=False).count(),
        "achievements": Achievement.objects.count(),
        "gallery": GalleryImage.objects.count(),
        "faqs": FAQ.objects.count(),
        "visitors_total": Visitor.objects.values("session_key").distinct().count(),
        "visitors_today": Visitor.objects.filter(first_seen__gte=today_start).values("session_key").distinct().count(),
    }

    # Visitors per day (last 7 days) for the line chart
    series = {}
    for i in range(6, -1, -1):
        series[(now - timedelta(days=i)).strftime("%a")] = 0
    rows = (
        Visitor.objects.filter(first_seen__gte=now - timedelta(days=7))
        .annotate(day=TruncDate("first_seen"))
        .values("day")
        .annotate(n=Count("session_key", distinct=True))
    )
    for row in rows:
        series[row["day"].strftime("%a")] = row["n"]

    project_choices = dict(Project._meta.get_field("category").choices)
    skill_choices = dict(Skill._meta.get_field("category").choices)
    project_rows = Project.objects.values("category").annotate(n=Count("id")).order_by("-n")
    skill_rows = Skill.objects.values("category").annotate(n=Count("id")).order_by("-n")

    context = {
        "stats": stats,
        "recent_messages": ContactMessage.objects.all()[:6],
        "visitors_chart": json.dumps({"labels": list(series.keys()), "values": list(series.values())}),
        "projects_chart": json.dumps(
            {"labels": [project_choices[r["category"]] for r in project_rows],
             "values": [r["n"] for r in project_rows]}
        ),
        "skills_chart": json.dumps(
            {"labels": [skill_choices[r["category"]] for r in skill_rows],
             "values": [r["n"] for r in skill_rows]}
        ),
    }
    return render(request, "admin/dashboard.html", context)


# ---------------------------------------------------------------------------
# Profile & Settings managers
# ---------------------------------------------------------------------------
@admin_required
def profile_edit(request):
    instance = Profile.load()
    form = ProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("core:profile_edit")
    return render(request, "admin/crud_form.html", {
        "resource": "profile",
        "section_title": "Profile Manager",
        "section_icon": "bi-person-fill",
        "form": form,
        "object": instance,
        "is_edit": True,
        "list_url": reverse("core:dashboard"),
    })


@admin_required
def settings_edit(request):
    instance = SiteSettings.load()
    form = SiteSettingsForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Settings saved.")
        return redirect("core:settings_edit")
    return render(request, "admin/crud_form.html", {
        "resource": "settings",
        "section_title": "Site Settings",
        "section_icon": "bi-gear-fill",
        "form": form,
        "object": instance,
        "is_edit": True,
        "list_url": reverse("core:dashboard"),
    })


# ---------------------------------------------------------------------------
# Generic CRUD
# ---------------------------------------------------------------------------
@admin_required
def crud(request, resource, action="list", pk=None):
    """One generic view handles list / add / edit / delete for every resource."""
    cfg = RESOURCES[resource]
    model, form_class = cfg["model"], cfg["form"]
    base = reverse(f"core:{resource}_list")

    if action == "list":
        qs = model.objects.all().order_by(*cfg.get("ordering", ("-updated_at",)))
        q = request.GET.get("q", "").strip()
        if q and cfg.get("search"):
            qs = qs.filter(**{f"{cfg['search']}__icontains": q})
        page_obj = Paginator(qs, cfg.get("page_size", 10)).get_page(request.GET.get("page"))
        rows = [
            {
                "cells": [
                    {"label": f.replace("_", " ").title(), "kind": kind, "value": value}
                    for f in cfg["fields"]
                    for kind, value in [_display_value(obj, f)]
                ],
                "edit_url": reverse(f"core:{resource}_edit", args=[obj.pk]),
                "delete_url": reverse(f"core:{resource}_delete", args=[obj.pk]),
            }
            for obj in page_obj
        ]
        return render(request, "admin/crud_list.html", {
            "resource": resource,
            "section_title": cfg["title"],
            "section_icon": cfg["icon"],
            "rows": rows,
            "page_obj": page_obj,
            "q": q,
            "total": model.objects.count(),
            "searchable": bool(cfg.get("search")),
            "create_url": reverse(f"core:{resource}_add"),
        })

    if action in ("add", "edit"):
        obj = get_object_or_404(model, pk=pk) if action == "edit" else None
        form = form_class(request.POST or None, request.FILES or None, instance=obj)
        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, f"{cfg['title']} saved successfully.")
            return redirect(base)
        return render(request, "admin/crud_form.html", {
            "resource": resource,
            "section_title": cfg["title"],
            "section_icon": cfg["icon"],
            "form": form,
            "object": obj,
            "is_edit": action == "edit",
            "list_url": base,
        })

    if action == "delete" and pk and request.method == "POST":
        model.objects.filter(pk=pk).delete()
        messages.success(request, "Entry deleted.")
    return redirect(base)


# ---------------------------------------------------------------------------
# Contact messages
# ---------------------------------------------------------------------------
@admin_required
def messages_list(request):
    qs = ContactMessage.objects.all()
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(subject__icontains=q))
    page_obj = Paginator(qs, 10).get_page(request.GET.get("page"))
    return render(request, "admin/messages.html", {
        "page_obj": page_obj,
        "q": q,
        "unread": ContactMessage.objects.filter(is_read=False).count(),
    })


@admin_required
def message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if not message.is_read:
        message.is_read = True
        message.save(update_fields=["is_read"])
    return render(request, "admin/message_detail.html", {"message": message})


@admin_required
def message_delete(request, pk):
    if request.method == "POST":
        ContactMessage.objects.filter(pk=pk).delete()
        messages.success(request, "Message deleted.")
    return redirect("core:messages_list")


@admin_required
def message_toggle(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method != "POST":
        return redirect("core:messages_list")
    message.is_read = not message.is_read
    message.save(update_fields=["is_read"])
    return redirect("core:messages_list")
