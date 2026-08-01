"""Public (viewer) views for the portfolio website."""
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .forms import ContactMessageForm
from .models import (
    Achievement, Certificate, Education, Experience, FAQ, GalleryImage,
    Project, Resume, Skill,
)


def home(request):
    """Landing page: hero, stats, previews of skills/projects/certificates."""
    context = {
        "featured_projects": Project.objects.filter(featured=True)[:3],
        "top_skills": Skill.objects.order_by("-level")[:8],
        "certificates": Certificate.objects.all()[:4],
        "achievements": Achievement.objects.all()[:3],
        "project_count": Project.objects.count(),
        "certificate_count": Certificate.objects.count(),
        "skill_count": Skill.objects.count(),
        "achievement_count": Achievement.objects.count(),
    }
    return render(request, "viewer/home.html", context)


def about(request):
    """Biography, career objective, education, mission and vision."""
    return render(
        request,
        "viewer/about.html",
        {"education": Education.objects.all(), "experiences": Experience.objects.all()},
    )


def skills(request):
    """Skills grouped by category."""
    grouped = {}
    for skill in Skill.objects.all():
        grouped.setdefault(skill.get_category_display(), []).append(skill)
    return render(request, "viewer/skills.html", {"categories": grouped})


def _paginate(request, queryset, per_page):
    page = Paginator(queryset, per_page).get_page(request.GET.get("page"))
    return page


def projects(request):
    """Project grid with search, category/status filters and pagination."""
    qs = Project.objects.all()
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    status = request.GET.get("status", "")
    if q:
        qs = qs.filter(title__icontains=q)
    if category:
        qs = qs.filter(category=category)
    if status:
        qs = qs.filter(status=status)
    return render(request, "viewer/projects.html", {
        "page_obj": _paginate(request, qs, 6),
        "q": q,
        "category": category,
        "status": status,
    })


def certificates(request):
    """Certificate grid with search and category filter."""
    qs = Certificate.objects.all()
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    if q:
        qs = qs.filter(title__icontains=q)
    if category:
        qs = qs.filter(category=category)
    return render(request, "viewer/certificates.html", {
        "page_obj": _paginate(request, qs, 8),
        "q": q,
        "category": category,
    })


def achievements(request):
    """Achievements with category filter."""
    qs = Achievement.objects.all()
    category = request.GET.get("category", "")
    if category:
        qs = qs.filter(category=category)
    return render(request, "viewer/achievements.html", {
        "page_obj": _paginate(request, qs, 8),
        "category": category,
    })


def gallery(request):
    """Public gallery with category filter."""
    qs = GalleryImage.objects.all()
    category = request.GET.get("category", "")
    if category:
        qs = qs.filter(category=category)
    return render(request, "viewer/gallery.html", {"page_obj": _paginate(request, qs, 12), "category": category})


def experience(request):
    """Work experience timeline."""
    return render(request, "viewer/experience.html", {"experiences": Experience.objects.all()})


def timeline(request):
    """Combined education + experience timeline, newest first."""
    items = []
    for edu in Education.objects.all():
        items.append({
            "year": edu.start_year,
            "type": "education",
            "title": edu.degree,
            "subtitle": edu.institution,
            "period": edu.year_range(),
            "description": edu.description,
        })
    for exp in Experience.objects.all():
        items.append({
            "year": exp.start_date.year,
            "type": "experience",
            "title": exp.role,
            "subtitle": exp.company,
            "period": exp.date_range(),
            "description": exp.description,
        })
    items.sort(key=lambda item: item["year"], reverse=True)
    return render(request, "viewer/timeline.html", {"timeline": items})


def resume(request):
    """Preview and download of the latest active resume."""
    return render(request, "viewer/resume.html", {"resume": Resume.latest()})


def contact(request):
    """Contact form (saved to the database, honeypot protected)."""
    form = ContactMessageForm(request.POST or None)
    if request.method == "POST":
        if request.POST.get("website"):  # honeypot filled -> bot, ignore silently
            return redirect(reverse("core:contact"))
        if form.is_valid():
            form.save()
            return redirect(reverse("core:contact") + "?sent=1")
    return render(request, "viewer/contact.html", {"form": form, "sent": request.GET.get("sent") == "1"})


@require_GET
def faq_api(request):
    """JSON endpoint powering the floating AI assistant (predefined FAQs only)."""
    faqs = FAQ.objects.all()
    return JsonResponse({
        "faqs": [
            {"id": f.pk, "question": f.question, "answer": f.answer, "keywords": f.keywords}
            for f in faqs
        ]
    })
